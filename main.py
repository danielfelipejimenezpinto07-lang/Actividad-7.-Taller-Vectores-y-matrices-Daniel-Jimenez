"""
Actividad 7 - Taller: Vectores y matrices
Autor: Daniel Jimenez Pinto y Valery Sofia Espitia Rodriguez

Este programa contiene la solución de los 5 ejercicios:
1. Ordenamiento burbuja de mayor a menor.
2. Determinante de una matriz NxN.
3. Sistema de examen de admisión.
4. Matriz de ventas por vendedor y año.
5. Actualización de tabla de clasificación de fútbol.
"""

import random
from dataclasses import dataclass


# ============================================================
# 1. ORDENAMIENTO BURBUJA DE MAYOR A MENOR
# ============================================================

def generar_arreglo(cantidad, minimo=1, maximo=100):
    """
    Genera un arreglo de números aleatorios.

    Args:
        cantidad (int): Cantidad de elementos del arreglo.
        minimo (int): Valor mínimo aleatorio.
        maximo (int): Valor máximo aleatorio.

    Returns:
        list: Arreglo generado.
    """
    if cantidad <= 0:
        raise ValueError("La cantidad de elementos debe ser mayor que cero.")

    return [random.randint(minimo, maximo) for _ in range(cantidad)]


def ordenar_burbuja_descendente(arreglo):
    """
    Ordena un arreglo de mayor a menor usando método burbuja.

    Args:
        arreglo (list): Lista de números.

    Returns:
        list: Lista ordenada de mayor a menor.
    """
    arreglo_ordenado = arreglo.copy()
    cantidad = len(arreglo_ordenado)

    for i in range(cantidad - 1):
        for j in range(cantidad - i - 1):
            if arreglo_ordenado[j] < arreglo_ordenado[j + 1]:
                arreglo_ordenado[j], arreglo_ordenado[j + 1] = (
                    arreglo_ordenado[j + 1],
                    arreglo_ordenado[j],
                )

    return arreglo_ordenado


# ============================================================
# 2. DETERMINANTE DE UNA MATRIZ NxN
# ============================================================

class Matrix:
    """
    Clase para representar una matriz cuadrada NxN.
    """

    def __init__(self, size):
        if size <= 0:
            raise ValueError("El tamaño de la matriz debe ser mayor que cero.")

        self.size = size
        self.data = [[0 for _ in range(size)] for _ in range(size)]

    def fill_matrix(self):
        """
        Llena la matriz con números aleatorios entre 1 y 20.
        """
        self.data = [
            [random.randint(1, 20) for _ in range(self.size)]
            for _ in range(self.size)
        ]

    def show_matrix(self):
        """
        Muestra la matriz en pantalla.
        """
        for row in self.data:
            print(row)

    def determinant(self):
        """
        Calcula el determinante de la matriz.

        Returns:
            int | float: Determinante de la matriz.
        """
        return calculate_determinant(self.data)


def calculate_determinant(matrix):
    """
    Calcula el determinante de una matriz cuadrada usando recursividad.

    Args:
        matrix (list): Matriz cuadrada.

    Returns:
        int | float: Determinante.
    """
    validate_square_matrix(matrix)

    size = len(matrix)

    if size == 1:
        return matrix[0][0]

    if size == 2:
        return (matrix[0][0] * matrix[1][1]) - (
            matrix[0][1] * matrix[1][0]
        )

    determinant = 0

    for column in range(size):
        minor = get_minor(matrix, 0, column)
        sign = (-1) ** column
        determinant += sign * matrix[0][column] * calculate_determinant(minor)

    return determinant


def get_minor(matrix, row_to_remove, column_to_remove):
    """
    Obtiene la submatriz eliminando una fila y una columna.

    Args:
        matrix (list): Matriz original.
        row_to_remove (int): Fila a eliminar.
        column_to_remove (int): Columna a eliminar.

    Returns:
        list: Submatriz.
    """
    minor = []

    for row_index, row in enumerate(matrix):
        if row_index != row_to_remove:
            new_row = [
                value
                for column_index, value in enumerate(row)
                if column_index != column_to_remove
            ]
            minor.append(new_row)

    return minor


def validate_square_matrix(matrix):
    """
    Valida que la matriz sea cuadrada.

    Args:
        matrix (list): Matriz a validar.
    """
    if not matrix:
        raise ValueError("La matriz no puede estar vacía.")

    size = len(matrix)

    for row in matrix:
        if len(row) != size:
            raise ValueError("La matriz debe ser cuadrada NxN.")


# ============================================================
# 3. EXAMEN DE ADMISIÓN
# ============================================================

@dataclass
class Student:
    credential: str
    math_answers: list
    verbal_answers: list


def generate_answer_key():
    """
    Genera el registro de respuestas correctas.
    Las primeras 30 son de matemática y las últimas 30 de verbal.

    Returns:
        list: Lista con 60 respuestas correctas.
    """
    return [random.randint(1, 5) for _ in range(60)]


def calculate_exam_scores(students, answer_key):
    """
    Calcula puntajes de matemática, verbal y total por estudiante.

    Args:
        students (list): Lista de estudiantes.
        answer_key (list): Respuestas correctas.

    Returns:
        list: Resultados de cada estudiante.
    """
    if len(answer_key) != 60:
        raise ValueError("El registro de respuestas correctas debe tener 60 campos.")

    results = []

    math_key = answer_key[:30]
    verbal_key = answer_key[30:]

    for student in students:
        if len(student.math_answers) != 30 or len(student.verbal_answers) != 30:
            raise ValueError("Cada estudiante debe tener 30 respuestas por examen.")

        math_score = count_correct_answers(student.math_answers, math_key)
        verbal_score = count_correct_answers(student.verbal_answers, verbal_key)
        total_score = math_score + verbal_score

        results.append({
            "credential": student.credential,
            "math_score": math_score,
            "verbal_score": verbal_score,
            "total_score": total_score,
        })

    return results


def count_correct_answers(student_answers, correct_answers):
    """
    Cuenta respuestas correctas.

    Args:
        student_answers (list): Respuestas del estudiante.
        correct_answers (list): Respuestas correctas.

    Returns:
        int: Número de respuestas correctas.
    """
    score = 0

    for student_answer, correct_answer in zip(student_answers, correct_answers):
        if student_answer == correct_answer:
            score += 1

    return score


def calculate_exam_statistics(results):
    """
    Calcula promedios, estudiantes sobre el promedio y mayor puntaje.

    Args:
        results (list): Resultados de estudiantes.

    Returns:
        dict: Estadísticas generales.
    """
    if not results:
        raise ValueError("Debe existir al menos un estudiante.")

    total_students = len(results)

    average_math = sum(item["math_score"] for item in results) / total_students
    average_verbal = sum(item["verbal_score"] for item in results) / total_students
    average_total = sum(item["total_score"] for item in results) / total_students

    students_above_average = [
        {
            "credential": item["credential"],
            "total_score": item["total_score"],
        }
        for item in results
        if item["total_score"] >= average_total
    ]

    best_student = max(results, key=lambda item: item["total_score"])

    return {
        "average_math": average_math,
        "average_verbal": average_verbal,
        "average_total": average_total,
        "students_above_average": students_above_average,
        "best_student": best_student,
    }


def generate_random_students(quantity):
    """
    Genera estudiantes con respuestas aleatorias para prueba de escritorio.

    Args:
        quantity (int): Cantidad de estudiantes.

    Returns:
        list: Lista de estudiantes.
    """
    if quantity <= 0:
        raise ValueError("La cantidad de estudiantes debe ser mayor que cero.")

    students = []

    for number in range(1, quantity + 1):
        credential = f"EST-{number:03d}"
        math_answers = [random.randint(1, 5) for _ in range(30)]
        verbal_answers = [random.randint(1, 5) for _ in range(30)]

        students.append(Student(credential, math_answers, verbal_answers))

    return students


# ============================================================
# 4. MATRIZ DE VENTAS
# ============================================================

def generate_sales_matrix(sellers, years, minimum_sale=1000, maximum_sale=10000):
    """
    Genera una matriz de ventas de N vendedores por M años.

    Args:
        sellers (int): Número de vendedores.
        years (int): Número de años.
        minimum_sale (int): Venta mínima.
        maximum_sale (int): Venta máxima.

    Returns:
        list: Matriz de ventas.
    """
    if sellers <= 0 or years <= 0:
        raise ValueError("La cantidad de vendedores y años debe ser mayor que cero.")

    return [
        [random.randint(minimum_sale, maximum_sale) for _ in range(years)]
        for _ in range(sellers)
    ]


def calculate_sales_by_seller(sales_matrix):
    """
    Calcula el total de ventas por vendedor.

    Args:
        sales_matrix (list): Matriz de ventas.

    Returns:
        list: Total vendido por cada vendedor.
    """
    return [sum(row) for row in sales_matrix]


def calculate_sales_by_year(sales_matrix):
    """
    Calcula el total de ventas por año.

    Args:
        sales_matrix (list): Matriz de ventas.

    Returns:
        list: Total vendido por cada año.
    """
    if not sales_matrix:
        raise ValueError("La matriz de ventas no puede estar vacía.")

    years = len(sales_matrix[0])
    totals_by_year = []

    for column in range(years):
        total = sum(row[column] for row in sales_matrix)
        totals_by_year.append(total)

    return totals_by_year


def calculate_grand_total_sales(sales_matrix):
    """
    Calcula el gran total de ventas de la empresa.

    Args:
        sales_matrix (list): Matriz de ventas.

    Returns:
        int: Total general de ventas.
    """
    return sum(sum(row) for row in sales_matrix)


# ============================================================
# 5. TABLA DE CLASIFICACIÓN DE FÚTBOL
# ============================================================

@dataclass
class Team:
    code: str
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    points: int

    @property
    def goal_difference(self):
        """
        Calcula la diferencia de gol.

        Returns:
            int: Goles a favor menos goles en contra.
        """
        return self.goals_for - self.goals_against


@dataclass
class Match:
    local_code: str
    local_goals: int
    visitor_code: str
    visitor_goals: int


def update_standings(teams, matches):
    """
    Actualiza la tabla de clasificación después de una fecha.

    Args:
        teams (dict): Diccionario de equipos.
        matches (list): Lista de partidos.

    Returns:
        list: Tabla ordenada.
    """
    for match in matches:
        if match.local_code not in teams or match.visitor_code not in teams:
            raise ValueError("Uno de los equipos del partido no existe.")

        local_team = teams[match.local_code]
        visitor_team = teams[match.visitor_code]

        local_team.played += 1
        visitor_team.played += 1

        local_team.goals_for += match.local_goals
        local_team.goals_against += match.visitor_goals

        visitor_team.goals_for += match.visitor_goals
        visitor_team.goals_against += match.local_goals

        if match.local_goals > match.visitor_goals:
            local_team.won += 1
            local_team.points += 3

            visitor_team.lost += 1

        elif match.local_goals < match.visitor_goals:
            visitor_team.won += 1
            visitor_team.points += 3

            local_team.lost += 1

        else:
            local_team.drawn += 1
            visitor_team.drawn += 1

            local_team.points += 1
            visitor_team.points += 1

    return sort_standings(teams)


def sort_standings(teams):
    """
    Ordena la tabla por puntos, diferencia de gol y goles a favor.

    Args:
        teams (dict): Diccionario de equipos.

    Returns:
        list: Equipos ordenados.
    """
    return sorted(
        teams.values(),
        key=lambda team: (
            team.points,
            team.goal_difference,
            team.goals_for,
        ),
        reverse=True,
    )


# ============================================================
# PRUEBAS DE ESCRITORIO
# ============================================================

def test_bubble_sort():
    print("\n--- Ejercicio 1: Ordenamiento burbuja ---")

    arreglo = [8, 3, 10, 1, 7]
    print("Arreglo original:", arreglo)

    arreglo_ordenado = ordenar_burbuja_descendente(arreglo)
    print("Arreglo ordenado:", arreglo_ordenado)


def test_determinant():
    print("\n--- Ejercicio 2: Determinante de matriz ---")

    matrix = [
        [2, 3],
        [1, 4],
    ]

    print("Matriz:")
    for row in matrix:
        print(row)

    determinant = calculate_determinant(matrix)
    print("Determinante:", determinant)


def test_exam():
    print("\n--- Ejercicio 3: Examen de admisión ---")

    answer_key = generate_answer_key()
    students = generate_random_students(5)

    results = calculate_exam_scores(students, answer_key)
    statistics = calculate_exam_statistics(results)

    print("\nResultados por estudiante:")
    for result in results:
        print(
            f"Credencial: {result['credential']} | "
            f"Matemática: {result['math_score']} | "
            f"Verbal: {result['verbal_score']} | "
            f"Total: {result['total_score']}"
        )

    print("\nPromedio matemática:", round(statistics["average_math"], 2))
    print("Promedio verbal:", round(statistics["average_verbal"], 2))
    print("Promedio total:", round(statistics["average_total"], 2))

    print("\nEstudiantes con puntaje superior o igual al promedio:")
    for student in statistics["students_above_average"]:
        print(student)

    print("\nMayor puntaje:")
    print(statistics["best_student"])


def test_sales():
    print("\n--- Ejercicio 4: Matriz de ventas ---")

    sales_matrix = [
        [1000, 2000, 3000],
        [1500, 2500, 3500],
        [2000, 3000, 4000],
    ]

    print("Matriz de ventas:")
    for row in sales_matrix:
        print(row)

    sales_by_seller = calculate_sales_by_seller(sales_matrix)
    sales_by_year = calculate_sales_by_year(sales_matrix)
    grand_total = calculate_grand_total_sales(sales_matrix)

    print("Total por vendedor:", sales_by_seller)
    print("Total por año:", sales_by_year)
    print("Gran total de ventas:", grand_total)


def test_football():
    print("\n--- Ejercicio 5: Tabla de fútbol ---")

    teams = {
        "NAL": Team("NAL", 0, 0, 0, 0, 0, 0, 0),
        "MIL": Team("MIL", 0, 0, 0, 0, 0, 0, 0),
        "AME": Team("AME", 0, 0, 0, 0, 0, 0, 0),
        "JUN": Team("JUN", 0, 0, 0, 0, 0, 0, 0),
    }

    matches = [
        Match("NAL", 2, "MIL", 1),
        Match("AME", 0, "JUN", 0),
    ]

    standings = update_standings(teams, matches)

    print("Tabla actualizada:")
    print("Código | PJ | PG | PE | PP | GF | GC | DG | Puntos")

    for team in standings:
        print(
            f"{team.code:6} | "
            f"{team.played:2} | "
            f"{team.won:2} | "
            f"{team.drawn:2} | "
            f"{team.lost:2} | "
            f"{team.goals_for:2} | "
            f"{team.goals_against:2} | "
            f"{team.goal_difference:2} | "
            f"{team.points:6}"
        )


def run_all_tests():
    """
    Ejecuta las pruebas de escritorio de los 5 ejercicios.
    """
    test_bubble_sort()
    test_determinant()
    test_exam()
    test_sales()
    test_football()


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":
    run_all_tests()
