from kafka import KafkaConsumer
import json
import tkinter as tk
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import numpy as np

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    'payments',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Listening for transactions...\n")

# Track transaction counts
fraud_transactions = {}
normal_transactions = {}

def is_fraudulent(transaction):
    """Check if transaction is fraudulent."""
    return transaction["amount"] > 3000  # Example rule

def update_graph(i):
    """Update graph and log."""
    try:
        message = next(consumer)
        transaction = message.value
        user_id = transaction.get("user_id", "Unknown")

        if is_fraudulent(transaction):
            fraud_transactions[user_id] = fraud_transactions.get(user_id, 0) + 1
            log_transaction(f"🚨 FRAUD: {transaction['transaction_id']} - ${transaction['amount']} ⚠️", "red")
        else:
            normal_transactions[user_id] = normal_transactions.get(user_id, 0) + 1
            log_transaction(f"✅ NORMAL: {transaction['transaction_id']} - ${transaction['amount']}", "blue")
    except Exception as e:
        log_transaction(f"Error: {str(e)}", "black")

    # Update graph
    users = list(set(fraud_transactions.keys()) | set(normal_transactions.keys()))
    fraud_counts = [fraud_transactions.get(user, 0) for user in users]
    normal_counts = [normal_transactions.get(user, 0) for user in users]
    x = np.arange(len(users))

    ax.clear()
    ax.bar(x - 0.2, normal_counts, width=0.4, color='blue', label='Normal')
    ax.bar(x + 0.2, fraud_counts, width=0.4, color='red', label='Fraud')
    ax.set_xlabel("User ID")
    ax.set_ylabel("Transaction Count")
    ax.set_title("Live Fraud Detection")
    ax.set_xticks(x)
    ax.set_xticklabels(users, rotation=45)
    ax.legend()
    ax.grid(axis='y')

def log_transaction(message, color):
    """Show transaction in scrolling log."""
    transaction_log.config(state=tk.NORMAL)
    transaction_log.insert(tk.END, message + "\n", color)
    transaction_log.tag_config(color, foreground=color)
    transaction_log.config(state=tk.DISABLED)
    transaction_log.yview(tk.END)

# Create GUI
root = tk.Tk()
root.title("Fraud Detection System")
root.geometry("900x600")

# Text log area
transaction_log = scrolledtext.ScrolledText(root, width=100, height=10, state=tk.DISABLED)
transaction_log.pack(pady=10)

# Matplotlib graph setup
fig, ax = plt.subplots(figsize=(7, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Animate chart
ani = animation.FuncAnimation(fig, update_graph, interval=2000)

# Start GUI
root.mainloop()
