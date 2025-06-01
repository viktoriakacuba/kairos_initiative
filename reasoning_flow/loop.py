from core.llm import call_llm
from core.memory import save_interaction, get_last_n

def run_reasoning_loop(user_input: str) -> dict:
    steps = []

    # Step 0: Подгружаем последние размышления (контекст)
    recent_memory = get_last_n(3)
    context_str = "\n".join([f"Q: {q}\nA: {a}" for q, a in recent_memory])

    # Step 1: Интерпретация цели
    prompt_goal = f"{context_str}\n\nUser's intention: {user_input}\nWhat is the underlying goal?"
    goal = call_llm(prompt_goal)
    steps.append({"step": "Goal Interpretation", "output": goal})

    # Step 2: Планирование
    prompt_plan = f"Goal: {goal}\nPlan the next 3 steps to approach it."
    plan = call_llm(prompt_plan)
    steps.append({"step": "Planning", "output": plan})

    # Step 3: Размышление
    prompt_reflection = f"Goal: {goal}\nPlan: {plan}\nNow reflect on it: risks, logic, next thoughts."
    reflection = call_llm(prompt_reflection)
    steps.append({"step": "Reflection", "output": reflection})

    # Step 4: Сохраняем размышление в память
    save_interaction(user_input, reflection)

    return {
        "input": user_input,
        "goal": goal,
        "plan": plan,
        "reflection": reflection,
        "steps": steps
    }
