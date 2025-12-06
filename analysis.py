import pandas as pd
import matplotlib.pyplot as plt

# 1. Загрузка датасета
df = pd.read_csv("data_cat_breeds.csv")

# 2. Базовый осмотр структуры
print("Первые строки датасета:")
print(df.head(), "\n")

print("Информация о столбцах:")
print(df.info(), "\n")

print("Краткая статистика по числовым столбцам:")
print(df.describe(), "\n")

# 3. Расчёт средних веса и продолжительности жизни по породе
df["mean_weight"] = (df["min_weight"] + df["max_weight"]) / 2
df["mean_life"] = (df["min_life_expectancy"] + df["max_life_expectancy"]) / 2

print("Породы с рассчитанными средними значениями:")
print(df[["name", "mean_weight", "mean_life"]].head(), "\n")

# 4. Визуализация распределения веса
plt.figure(figsize=(8, 5))
plt.hist(df["mean_weight"], bins=10, edgecolor="black")
plt.xlabel("Средний вес породы, кг")
plt.ylabel("Количество пород")
plt.title("Распределение среднего веса пород кошек")
plt.tight_layout()
plt.show()

# 5. Визуализация зависимости «вес — продолжительность жизни»
plt.figure(figsize=(8, 5))
plt.scatter(df["mean_weight"], df["mean_life"])
plt.xlabel("Средний вес породы, кг")
plt.ylabel("Средняя продолжительность жизни, лет")
plt.title("Связь веса породы и продолжительности жизни кошек")
plt.grid(True)
plt.tight_layout()
plt.show()

# 6. Проверка гипотезы через корреляцию
corr = df["mean_weight"].corr(df["mean_life"])
print("Корреляция между средним весом и средней продолжительностью жизни:", corr)

if corr < 0:
    print("Гипотеза о отрицательной связи веса и продолжительности жизни частично подтверждается (корреляция отрицательная).")
else:
    print("Гипотеза о отрицательной связи веса и продолжительности жизни не подтверждается (корреляция неотрицательная).")

