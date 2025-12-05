import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import arff
import pandas as pd
import random
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

class TreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ARFF Tree Explorer")
        self.root.geometry("900x650")
        self.file_path = None
        self.data = None

        tk.Label(root, text="ARFF Tree Explorer", font=("Arial", 18, "bold")).pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=5)

        tk.Button(frame, text="\U0001F4C2 Load ARFF File", command=self.load_arff, width=20, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(frame, text="\U0001F4C8 Compare Algorithms", command=self.compare_algorithms, width=20, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5)

        tree_frame = tk.Frame(root)
        tree_frame.pack(pady=5)

        tk.Label(tree_frame, text="\U0001F333 Select Model to Show Tree:").grid(row=0, column=0, padx=5)

        self.model_choice = ttk.Combobox(tree_frame, values=["J48 Tree", "REPTree", "Decision Stump", "Random Forest"])
        self.model_choice.set("J48 Tree")
        self.model_choice.grid(row=0, column=1, padx=5)

        tk.Button(tree_frame, text="Show Tree", command=self.show_selected_tree, width=15, bg="#FF9800", fg="white").grid(row=0, column=2, padx=5)

        self.output_text = tk.Text(root, height=25, width=110, font=("Courier", 10))
        self.output_text.pack(pady=10)

    def load_arff(self):
        file = filedialog.askopenfilename(filetypes=[("ARFF files", "*.arff")])
        if file:
            self.file_path = file
            with open(file, 'r') as f:
                raw_data = arff.load(f)
            df = pd.DataFrame(raw_data['data'], columns=[attr[0] for attr in raw_data['attributes']])
            for col in df.columns:
                if df[col].dtype == object:
                    df[col] = LabelEncoder().fit_transform(df[col])
            self.data = df
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"\u2705 Loaded ARFF file: {file}\n")

    def compare_algorithms(self):
        if self.data is None:
            messagebox.showerror("Error", "Please load an ARFF file first.")
            return

        X = self.data.iloc[:, :-1]
        y = self.data.iloc[:, -1]

        models = {
            "J48 Tree": DecisionTreeClassifier(criterion='entropy'),
            "REPTree": DecisionTreeClassifier(max_depth=5, min_samples_leaf=5),
            "Random Forest": RandomForestClassifier(n_estimators=5),
            "Decision Stump": DecisionTreeClassifier(max_depth=1),
            "Logistic Model Tree (LMT approx)": LogisticRegression(max_iter=1000)
        }

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"{'Model':<40}{'Accuracy (CV)':>20}\n")
        self.output_text.insert(tk.END, f"{'-'*60}\n")

        best_models = []
        best_accuracy = 0.0
        results = {}

        for name, model in models.items():
            try:
                scores = cross_val_score(model, X, y, cv=5)
                avg_acc = scores.mean()
                results[name] = avg_acc
                self.output_text.insert(tk.END, f"{name:<40}{avg_acc*100:>17.2f}%\n")

                if avg_acc > best_accuracy:
                    best_accuracy = avg_acc
                    best_models = [name]
                elif avg_acc == best_accuracy:
                    best_models.append(name)
            except Exception as e:
                self.output_text.insert(tk.END, f"{name:<40} Failed: {str(e)}\n")

        best_models_str = ", ".join(best_models)
        self.output_text.insert(tk.END, f"\n\u2728 Best Performing Model(s): {best_models_str} ({best_accuracy*100:.2f}%)\n")

    def show_selected_tree(self):
        if self.data is None:
            messagebox.showerror("Error", "Please load an ARFF file first.")
            return

        model_name = self.model_choice.get()
        X = self.data.iloc[:, :-1]
        y = self.data.iloc[:, -1]

        if model_name == "J48 Tree":
            model = DecisionTreeClassifier(criterion='entropy')
            model.fit(X, y)
            plt.figure(figsize=(15, 10))
            plot_tree(model, feature_names=X.columns, class_names=[str(cls) for cls in model.classes_], filled=True)
            plt.title(f"{model_name} Visualization")
            plt.tight_layout()
            plt.show()

        elif model_name == "REPTree":
            model = DecisionTreeClassifier(max_depth=5, min_samples_leaf=5)
            model.fit(X, y)
            plt.figure(figsize=(15, 10))
            plot_tree(model, feature_names=X.columns, class_names=[str(cls) for cls in model.classes_], filled=True)
            plt.title(f"{model_name} Visualization")
            plt.tight_layout()
            plt.show()

        elif model_name == "Decision Stump":
            model = DecisionTreeClassifier(max_depth=1)
            model.fit(X, y)
            plt.figure(figsize=(15, 10))
            plot_tree(model, feature_names=X.columns, class_names=[str(cls) for cls in model.classes_], filled=True)
            plt.title(f"{model_name} Visualization")
            plt.tight_layout()
            plt.show()

        elif model_name == "Random Forest":
            model = RandomForestClassifier(n_estimators=10)
            model.fit(X, y)
            total_trees = len(model.estimators_)
            selected_indexes = random.sample(range(total_trees), min(3, total_trees))
            for idx in selected_indexes:
                estimator = model.estimators_[idx]
                plt.figure(figsize=(15, 10))
                plot_tree(estimator, feature_names=X.columns, class_names=[str(cls) for cls in model.classes_], filled=True)
                plt.title(f"Random Forest - Tree {idx + 1}")
                plt.tight_layout()
                plt.show()
        else:
            messagebox.showerror("Error", "Model visualization not supported.")

# ===== Run App =====
if __name__ == "__main__":
    root = tk.Tk()
    app = TreeApp(root)
    root.mainloop()
