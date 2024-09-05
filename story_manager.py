import json
import re
import os
import logging
import random
from text_utils import generate_text
from templates import PROMPT_TEMPLATES
from ui_utils import select_template
from config import MAX_HISTORY_CONTEXT, RECORDINGS_DIR, MAX_TITLE_WORDS

logger = logging.getLogger(__name__)

class StoryManager:
    def __init__(self):
        self.story_title = ""
        self.episode_count = 1
        self.story_history = []
        self.current_template = ""
        self.last_choice = None
        self.last_response = None
        self.used_elements = set()
        self.used_questions = set()

    def start_new_story(self):
        self.story_title = ""
        self.episode_count = 1
        self.story_history = []
        self.current_template = select_template()
        self.last_choice = None
        self.last_response = None
        self.used_elements.clear()
        self.used_questions.clear()
        logger.info(f"Started a new story with template: {self.current_template}")

    def load_story(self):
        while True:
            try:
                save_files = [f for f in os.listdir() if f.endswith('.json')]
                if not save_files:
                    logger.info("No save files found. Starting a new story.")
                    self.start_new_story()
                    return

                print("\nAvailable save files:")
                for i, file in enumerate(save_files, 1):
                    print(f"{i}. {file}")
                print(f"{len(save_files) + 1}. Start a new story")

                choice = input("Enter the number of the file to load, or 'new' to start a new story: ").strip()

                if choice.lower() == 'new' or choice == str(len(save_files) + 1):
                    self.start_new_story()
                    return

                file_index = int(choice) - 1
                if 0 <= file_index < len(save_files):
                    filename = save_files[file_index]
                    self._load_story_from_file(filename)
                    return
                else:
                    logger.warning("Invalid choice. Please try again.")
            except ValueError:
                logger.warning("Invalid input. Please enter a number or 'new'.")
            except Exception as e:
                logger.error(f"Unexpected error in load_story: {e}")

    def _load_story_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.story_title = data['title']
                self.episode_count = data['episode_count']
                self.story_history = data['history']
                self.current_template = data['template']
                self.last_choice = data.get('last_choice', None)
                self.last_response = data.get('last_response', None)
                self.used_elements = set(data.get('used_elements', []))
                self.used_questions = set(data.get('used_questions', []))
            logger.info(f"Loaded story: {self.story_title}")
        except FileNotFoundError:
            logger.error(f"File '{filename}' not found.")
        except json.JSONDecodeError:
            logger.error(f"Error reading file '{filename}'. It may be corrupted.")
        except KeyError as e:
            logger.error(f"Error loading story from '{filename}'. Missing key: {e}")

    def save_story(self):
        if not self.story_title:
            logger.warning("No story to save. Please start a new story first.")
            return
        
        clean_title = re.sub(r'[^\w\-_\. ]', '_', self.story_title)
        clean_title = re.sub(r'\s+', '_', clean_title)
        clean_title = clean_title[:50]  # Limit to 50 characters
        
        filename = f"{clean_title}.json"
        data = {
            'title': self.story_title,
            'episode_count': self.episode_count,
            'history': self.story_history,
            'template': self.current_template,
            'last_choice': self.last_choice,
            'last_response': self.last_response,
            'used_elements': list(self.used_elements),
            'used_questions': list(self.used_questions)
        }
        try:
            with open(filename, 'w') as f:
                json.dump(data, f)
            logger.info(f"Story saved successfully as '{filename}'.")
        except IOError as e:
            logger.error(f"Error saving story: {e}")

    def generate_recap(self):
        if len(self.story_history) < 2:
            logger.info("Not enough history for a recap.")
            return "The story has just begun!"
        
        recent_history = self.story_history[-MAX_HISTORY_CONTEXT:]
        context = ". ".join(recent_history)
        
        recap_prompt = f"Provide a brief recap of the recent events in the story titled '{self.story_title}'. Here's the recent context: {context}"
        
        try:
            recap = generate_text(recap_prompt)
            logger.info("Recap generated successfully.")
            return recap
        except Exception as e:
            logger.error(f"Error generating recap: {e}")
            return "Error: Unable to generate recap."

    def generate_narrative(self, image_description):
        try:
            if not self.story_title:
                title_prompt = f"Create a short and catchy title (max {MAX_TITLE_WORDS} words) for a {self.current_template} series based on this description: {image_description}."
                self.story_title = generate_text(title_prompt)
                logger.info(f"New Series: {self.story_title}")

            context = self._get_relevant_context()
            
            if self.episode_count % 5 == 0:  # Generate a recap every 5 episodes
                recap = self.generate_recap()
                print("Recap of recent events:")
                print(recap)
            
            if self.current_template == "life-captions":
                question_type = None
            else:
                question_type = "multiple_choice" if random.random() < 0.7 else "open_ended"
            
            narration_prompt = self._generate_diverse_prompt(image_description, context, question_type)
            
            response = generate_text(narration_prompt)
            
            narrative, questions = self._separate_narrative_and_questions(response, question_type)
            
            if not questions and question_type is not None:
                questions = self._generate_fallback_questions(narrative, question_type)
            
            self._update_used_elements(narrative)
            self.story_history.append(narrative)
            
            return narrative, questions, question_type
        except KeyError:
            logger.error(f"Invalid template: {self.current_template}")
            return "Error: Invalid storytelling template.", None, None
        except Exception as e:
            logger.error(f"Error generating narrative: {e}")
            return "Error: Unable to generate narrative.", None, None

    def _get_relevant_context(self):
        recent_history = self.story_history[-MAX_HISTORY_CONTEXT:]
        context = ". ".join(recent_history)
        if self.last_choice:
            context += f" Last choice: {self.last_choice}."
        if self.last_response:
            context += f" Last response: {self.last_response}."
        return context

    def _generate_diverse_prompt(self, image_description, context, question_type):
        base_prompt = PROMPT_TEMPLATES[self.current_template].format(
            title=self.story_title,
            episode=self.episode_count,
            description=image_description,
            context=context,
            last_choice=self.last_choice if self.last_choice else "None",
            last_response=self.last_response if self.last_response else "None",
            question_type=question_type
        )
        
        diversity_prompt = f"""
        {base_prompt}
        
        Please ensure the response is diverse and different from previous episodes. 
        Avoid repeating these elements: {', '.join(self.used_elements)}
        Introduce new characters, locations, or plot elements to keep the story fresh and engaging.
        Generate entirely new and unique questions that haven't been asked before.
        Previous questions (avoid these): {', '.join(self.used_questions)}
        
        Important: Generate ONLY {'multiple-choice questions (A, B, C, D)' if question_type == 'multiple_choice' else 'one open-ended question'}. Do not mix question types.
        """
        
        return diversity_prompt

    def _separate_narrative_and_questions(self, response, question_type):
        if question_type == "multiple_choice":
            parts = re.split(r'\n[A-D]\)', response, 1)
            if len(parts) == 2:
                narrative = parts[0].strip()
                questions = "A)" + parts[1].strip()
            else:
                narrative = response
                questions = ""
        elif question_type == "open_ended":
            sentences = response.split('.')
            if len(sentences) > 1:
                narrative = '.'.join(sentences[:-1]).strip() + '.'
                questions = sentences[-1].strip()
            else:
                narrative = response
                questions = ""
        else:
            narrative = response
            questions = ""
        
        self._update_used_questions(questions)
        return narrative, questions

    def _generate_fallback_questions(self, narrative, question_type):
        fallback_prompt = f"""
        Based on the following narrative, generate {'four multiple-choice questions (A, B, C, D)' if question_type == 'multiple_choice' else 'one open-ended question'} that encourage the reader to think critically about the story and make decisions about what should happen next:

        Narrative: {narrative}

        Ensure the questions are unique and haven't been asked before.
        Previous questions (avoid these): {', '.join(self.used_questions)}
        """
        
        questions = generate_text(fallback_prompt)
        self._update_used_questions(questions)
        return questions

    def _update_used_elements(self, response):
        words = re.findall(r'\b\w+\b', response.lower())
        self.used_elements.update(word for word in words if len(word) > 5)  # Only add words longer than 5 characters
        if len(self.used_elements) > 100:  # Limit the size of used_elements
            self.used_elements = set(random.sample(list(self.used_elements), 50))

    def _update_used_questions(self, questions):
        if questions:
            self.used_questions.add(questions)
        if len(self.used_questions) > 20:  # Limit the size of used_questions
            self.used_questions = set(random.sample(list(self.used_questions), 10))

    def process_player_choice(self, player_choice, image_description):
        self.last_choice = player_choice
        self.last_response = None
        return self._process_player_input(player_choice, image_description, is_choice=True)

    def process_player_response(self, player_response, image_description):
        self.last_choice = None
        self.last_response = player_response
        return self._process_player_input(player_response, image_description, is_choice=False)

    def _process_player_input(self, player_input, image_description, is_choice):
        try:
            input_type = "choice" if is_choice else "response"
            context = self._get_relevant_context()
            
            input_prompt = f"""
            Based on the player's {input_type}: "{player_input}", continue the story.
            Previous context: {context}
            Current scene: {image_description}
            
            Describe the outcome of their {input_type} and set up the next scene or challenge in 2-3 sentences.
            Ensure that the story progresses and changes based on this {input_type}.
            Avoid repeating these elements: {', '.join(self.used_elements)}
            Introduce new characters, locations, or plot elements to keep the story fresh and engaging.
            """
            
            outcome = generate_text(input_prompt)
            self._update_used_elements(outcome)
            self.story_history.append(f"Player {input_type}: {player_input}")
            self.story_history.append(f"Outcome: {outcome}")
            return outcome
        except Exception as e:
            logger.error(f"Error processing player {input_type}: {e}")
            return f"Error: Unable to process player {input_type}."
