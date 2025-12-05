# 📘 **ARFF Tree Explorer**  
*A Python-Based Machine Learning Visualization Tool for ARFF Datasets*

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Framework-Tkinter-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/ML-Library-Scikit--Learn-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/File_Format-ARFF-yellow?style=for-the-badge">
  <img src="https://img.shields.io/badge/Visualization-Matplotlib-red?style=for-the-badge">
</p>

---

## 🚀 **Overview**

**ARFF Tree Explorer** is a Python-based desktop application designed to load **ARFF datasets**, train **multiple classification models**, and visualize **decision trees** in an intuitive, beginner-friendly GUI.

The tool makes learning ML more accessible by combining:

- Python GUI (Tkinter)  
- ARFF file processing  
- Decision tree visualization  
- Classifier performance comparison  
- User-friendly workflow for education & research  

This system acts as a lightweight, open-source alternative to Weka.

---

## 🎯 **Key Features**

### **🔹 Classifier Comparison Module**
- Load ARFF files  
- Automatic preprocessing  
- Evaluate models using **5-fold cross-validation**  
- Compare accuracy of:
  - J48 (Entropy-based Decision Tree)  
  - REPTree  
  - Random Forest  
  - Decision Stump  
  - Logistic Regression (LMT Approximation)  

---

### **🔹 Decision Tree Visualization Module**
- Select model from dropdown  
- Train automatically  
- Visualize decision trees using Matplotlib  
- Explore splits, nodes, and decision paths  

---

### **🔹 Core System**
- Built fully in **Python**  
- Handles categorical encoding  
- Model training + evaluation in real-time  
- Simple, minimal, student-friendly interface  

---

## 🧩 **System Architecture**

```
User GUI (Tkinter)
        │
Data Processing (Pandas + ARFF Loader)
        │
Model Training (Scikit-learn)
        │
Classifier Comparison / Tree Visualization
        │
Matplotlib Output (Decision Trees)
```

---

## 🛠️ **Tools & Technologies**

| Component   | Technology |
|-------------|------------|
| Language    | Python 3.x |
| GUI         | Tkinter |
| ML Models   | Scikit-learn |
| Data Loader | scipy.io.arff |
| Visualization | Matplotlib |
| IDE         | VS Code |

---

## 📁 **Project Structure**

```
ARFF-Tree-Explorer/
├─ main.py
├─ assets/
│   ├─ screenshots/
│   └─ icons/
├─ sample_datasets/
├─ requirements.txt
└─ README.md
```

---

## ⚙️ **Installation & Setup**

### **1️⃣ Install Dependencies**
```bash
pip install pandas scikit-learn matplotlib scipy
```

### **2️⃣ Run the Application**
```bash
python main.py
```

---

## 🔍 **How It Works**

### **User Workflow**
1. Upload ARFF file  
2. System loads → preprocesses data  
3. Compare classifiers  
4. Visualize decision trees  

### **Behind the Scenes**
- ARFF parsed using `scipy.io.arff`  
- Categorical features encoded with `LabelEncoder`  
- Models trained via Scikit-learn  
- Tree visualized using `plot_tree()`  

---

## 🧠 **Algorithms Used**

### **📌 Classifier Comparison Algorithm**
- Evaluates multiple ML models  
- Uses 5-fold cross-validation  
- Outputs accuracy scores  

### **📌 Decision Tree Visualization Algorithm**
- Trains selected classifier  
- Generates complete tree plot  
- Supports J48, REPTree, RandomForest, etc.

---

# 🗂️ **Flowchart**
![Flowchart](https://drive.google.com/uc?export=view&id=1obfMWwPutTZKcPcoVI9ojAxZlUl8rXpT)

---

# 📸 **Demo Preview**

### **🏠 Home Page**
![Home Page](https://drive.google.com/uc?export=view&id=1IznJGMQeC-MaQHC7CWBVKJJ-od1O5w4F)

### **📊 Classifier Comparison Module**
![Classifier Comparison Module](https://drive.google.com/uc?export=view&id=1Gwip2d5pp4L6DVw_zYlBACKoAdpR6DDS)

### **🌳 Decision Tree Visualization Module**
![Decision Tree Visualization Module](https://drive.google.com/uc?export=view&id=1RJEtSc6qZ_dLksylsHbX6q6mlqlDIaHe)

### **🌲 J48 Tree Visualization**
![J48 Tree Visualization Module](https://drive.google.com/uc?export=view&id=1vr-ku4Lq1Ja9mutwV1PDis9JfLC6mDLw)

---

## 📈 **Performance Evaluation**

- Fast dataset loading  
- Accurate ML model comparison  
- Clear visual decision trees  
- Smooth GUI interaction  
- Tested on multiple UCI ARFF datasets  

---

## ⚠️ **Limitations**

- Only ARFF supported (no CSV/XLSX)  
- GUI may freeze with large datasets  
- No threading / background tasks  
- No exporting of tree images  
- No hyperparameter tuning  

---

## 🔮 **Future Improvements**

- Support CSV, XLSX, JSON  
- Multi-threading for large data  
- Save/Export trees  
- Add hyperparameter tuning panel  
- Zoomable, interactive tree viewer  
- Dark mode for GUI  

---

## 📄 **Full Project Report (PDF)**  
*(Complete documentation, flowcharts, case studies, screenshots)*

👉 **Download:**  
[Download / View Project Report (PDF)](https://drive.google.com/file/d/1KPGYReB1CeF6NDjE-e4hWnhvzhUHXjWp/view?usp=drive_link)

---

## 👥 **Authors**

- **Md. Zehadul Islam**  
- **Md. Abdullah Al Moin**
