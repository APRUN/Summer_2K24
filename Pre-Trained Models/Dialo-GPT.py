!pip install transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer=AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model=AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

def run(user_text,chat_history_ids):
  input_ids=tokenizer.encode(user_text+tokenizer.eos_token,return_tensors="pt")
  if chat_history_ids is None:
    bot_input_ids=input_ids
  else:
    bot_input_ids=torch.cat([chat_history_ids,input_ids],dim=-1)
  chat_history_ids=model.generate(bot_input_ids,max_length=1000,pad_token_id=tokenizer.eos_token_id)
  resp=tokenizer.decode(chat_history_ids[:,bot_input_ids.shape[-1]:][0],skip_special_tokens=True)
  return resp,chat_history_ids

def main():
    chat_history_ids = None
    print("DialoGPT Chatbot: Hello! How can I help you today?")
    while True:

      user_input = input("You: ")
      if user_input.lower() in ['exit', 'quit']:
          break
      response, chat_history_ids = run(user_input, chat_history_ids)
      print("DialoGPT Chatbot:", response)

if __name__ == "__main__":
    main()