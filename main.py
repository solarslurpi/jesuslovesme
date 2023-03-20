from lightshine import InspirationGenerator


### Create an instance of the InspirationGenerator class ###
gen = InspirationGenerator()
topic = None
while not topic:
    topic = gen.ask_topic()
print(f"What does Jesus think about {topic}? ")
prompt = gen.create_prompt()
loving_words = gen.generate(prompt)
print(loving_words)