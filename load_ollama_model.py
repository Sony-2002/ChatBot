from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    AutoConfig,
    Trainer,
    TrainingArguments,
    TextDataset,
    DataCollatorForLanguageModeling,
)
import os

# Step 1: Define model and tokenizer
MODEL_NAME = "gpt2"  # Replace with your base model
SAVE_DIR = "/Users/sony/Desktop/vscode/project_code/models/ollama_finetuned"

# Load pre-trained model and tokenizer
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Ensure the save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Step 2: Prepare dataset
def load_dataset(file_path, tokenizer, block_size=128):
    dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=block_size,
    )
    return dataset

# Example training file (prepare a text file for fine-tuning)
TRAIN_FILE = "/Users/sony/Desktop/vscode/project_code/models/ollama_finetuned/training_data.txt"  # Replace with your dataset file path

# Check if training data exists
if not os.path.exists(TRAIN_FILE):
    with open(TRAIN_FILE, "w") as f:
        f.write("This is an example fine-tuning dataset.\nThis chatbot is amazing.\n")

train_dataset = load_dataset(TRAIN_FILE, tokenizer)

# Step 3: Define data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,  # Masked Language Model is false for causal language models
)

# Step 4: Configure training
training_args = TrainingArguments(
    output_dir="./results",  # Output directory
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=10_000,
    save_total_limit=2,
    prediction_loss_only=True,
    logging_dir="./logs",  # Logging directory
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

# Step 5: Train the model
trainer.train()

# Step 6: Save model, tokenizer, and config
model.save_pretrained(SAVE_DIR)
tokenizer.save_pretrained(SAVE_DIR)

# Save custom configuration if needed
config = AutoConfig.from_pretrained(MODEL_NAME)
config.save_pretrained(SAVE_DIR)

print(f"Model, tokenizer, and config saved to: {SAVE_DIR}")
