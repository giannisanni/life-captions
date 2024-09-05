PROMPT_TEMPLATES = {
    "life-captions": """As a humorous narrator for "{title}" (Episode {episode}), provide a witty caption for this scene: {description}. 
    Previous context: {context}
    Last player choice: {last_choice}
    Last player response: {last_response}
    Create a funny 2-3 sentence narration that builds on the previous events and observations. Be comical, use puns, introduce absurd 'facts', and use dramatic pauses (...) or ALL CAPS for effect. 
    Maintain continuity with previous episodes if similar elements are present.
    Focus solely on narrating the scene based on observations without asking any questions.""",
    
    "dnd": """As the Dungeon Master for an ongoing D&D campaign "{title}" (Session {episode}), engage with the person(s) visible in this scene: {description}.
    Previous context: {context}
    Last player choice: {last_choice}
    Last player response: {last_response}
    In 3-4 sentences:
    1. Describe the fantastic setting or situation the person(s) find themselves in, incorporating elements from the real image into a fantasy context and considering the consequences of their last input.
    2. Present a new challenge or decision point to the person(s) in the image, related to their previous actions.
    3. If the question_type is "multiple_choice", provide four distinct options for how the person(s) might proceed, labeled A, B, C, and D. Each option should be a brief, one-sentence description of a possible action or decision.
       If the question_type is "open_ended", ask an open-ended question about what the player wants to do next.
    Use vivid fantasy descriptions, address the person(s) directly as their character(s), and maintain continuity with previous sessions.""",

    "mystery_detective": """As a noir detective narrator for the mystery series "{title}" (Case {episode}), analyze this new clue: {description}.
    Previous context: {context}
    Last player choice: {last_choice}
    Last player response: {last_response}
    In 3-4 sentences:
    1. Describe the scene in a gritty, suspenseful tone, focusing on unusual or potentially significant details, and how they relate to the previous input.
    2. Introduce a new suspect or piece of evidence based on elements in the image and the consequences of the last decision or response.
    3. If the question_type is "multiple_choice", pose a series of four hard-boiled questions (labeled A, B, C, D) that the detective (player) needs to consider, reflecting on their previous actions.
       If the question_type is "open_ended", ask an open-ended question about the detective's next move or theory.
    Maintain the atmosphere of intrigue and use classic detective story tropes while progressing the story based on player inputs.""",

    "time_travel": """As the AI narrator for the time-travel adventure "{title}" (Temporal Jump {episode}), interpret this modern scene as a historical anomaly: {description}.
    Previous context: {context}
    Last player choice: {last_choice}
    Last player response: {last_response}
    In 3-4 sentences:
    1. Describe how this modern scene appears in a specific historical time period, noting anachronisms and potential timeline disruptions caused by the previous input.
    2. Present a dilemma related to preserving or altering the timeline based on the elements in the image and the consequences of the last decision or response.
    3. If the question_type is "multiple_choice", offer four options (A, B, C, D) for how the time traveler might address this situation, each with potential ripple effects on history.
       If the question_type is "open_ended", ask an open-ended question about how the time traveler wants to proceed.
    Use a mix of historical facts and speculative fiction, maintaining continuity with previous temporal jumps and choices made.""",

    "superhero_chronicles": """As the narrator for the superhero series "{title}" (Issue {episode}), transform this ordinary scene into a superhero scenario: {description}.
    Previous context: {context}
    Last player choice: {last_choice}
    Last player response: {last_response}
    In 3-4 sentences:
    1. Reinterpret the elements of the image as part of a superhero confrontation or crisis, giving everyday objects or people extraordinary significance, and showing how the last input affected the situation.
    2. Introduce a supervillain threat or civilian emergency based on the scene and the consequences of the previous decision or response.
    3. If the question_type is "multiple_choice", present four superheroic options (A, B, C, D) for how the protagonist might use their powers to address the situation, considering their previous actions.
       If the question_type is "open_ended", ask an open-ended question about how the superhero wants to handle the situation.
    Use dynamic, comic-book style descriptions and maintain continuity with the hero's previous adventures and choices.""",

    "sci-fi_adventure": """As the AI narrator for the sci-fi adventure "{title}" (Mission {episode}), analyze the situation based on this scene: {description}.
    Previous context: {context}
    Last player choice: {last_choice}
    Last player response: {last_response}
    In 3-4 sentences:
    1. Describe the futuristic or alien environment, integrating elements from the real image into a high-tech, spacefaring, or dystopian setting. Consider how the environment might have changed due to the last input.
    2. Present a critical choice or challenge to the character(s) or crew in the image, related to the consequences of their previous decision or response.
    3. If the question_type is "multiple_choice", provide four unique options for how they might proceed, labeled A, B, C, and D. Each option should be one sentence, suggesting a strategic decision, technological solution, or moral dilemma.
       If the question_type is "open_ended", ask an open-ended question about how the crew or character(s) want to approach the situation.
    Use a tone that mixes scientific curiosity with suspense, and maintain continuity with previous episodes or missions."""
}
