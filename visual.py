import detector as det
import matplotlib.pyplot as plt
import seaborn as sns   


def plot_chart(logs):
    actions = [log['action'] for log in logs]
    action_counts = {action: actions.count(action) for action in set(actions)}

    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(action_counts.keys()), y=list(action_counts.values()), palette="viridis")
    plt.title("Log Action Frequency")
    plt.xlabel("Action")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
def bar_chart(logs):
    actions = [log['action'] for log in logs]
    action_counts = {action: actions.count(action) for action in set(actions)}

    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(action_counts.keys()), y=list(action_counts.values()), palette="magma")
    plt.title("Log Action Frequency - Bar Chart")
    plt.xlabel("Action")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
def pie_chart(logs):
    actions = [log['action'] for log in logs]
    action_counts = {action: actions.count(action) for action in set(actions)}

    plt.figure(figsize=(8, 8))
    plt.pie(action_counts.values(), labels=action_counts.keys(), autopct='%1.1f%%', colors=sns.color_palette("pastel"))
    plt.title("Log Action Distribution - Pie Chart")
    plt.tight_layout()
    plt.show()


def main():
    logs = det.generate_fake_logs(200)
    plot_chart(logs)
    bar_chart(logs)
    pie_chart(logs)
    
if __name__ == "__main__":
    main()
    




