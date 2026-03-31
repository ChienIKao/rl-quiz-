import json
import random
import re
from html import escape
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


PAGE_TITLE = "強化學習測驗"
POINTS_PER_QUESTION = 2
QUESTION_BANK_PATH = Path(__file__).resolve().parent / "data" / "questions.json"


def load_questions() -> list[dict]:
    return json.loads(QUESTION_BANK_PATH.read_text(encoding="utf-8"))


def format_math_text(text: str) -> str:
    formatted = text.strip()
    formatted = re.sub(r"(?ms)^\[\s*\n(.*?)\n\]$", lambda m: f"$$\n{m.group(1).strip()}\n$$", formatted)
    formatted = re.sub(r"(?ms)\n\[\s*\n(.*?)\n\]", lambda m: f"\n\n$$\n{m.group(1).strip()}\n$$\n", formatted)
    formatted = re.sub(r"(?<![\s(（「『])(\$[^$\n]+\$)", r" \1", formatted)
    formatted = re.sub(r"(\$[^$\n]+\$)(?![\s)）」。、，；：！？』])", r"\1 ", formatted)
    formatted = re.sub(r"[ \t]{2,}", " ", formatted)
    return formatted.strip()


def estimate_html_height(text: str, font_size: int = 18) -> int:
    """Estimate iframe height accounting for CJK vs ASCII character widths."""
    line_h = round(font_size * 1.7)   # line-height:1.5 + generous buffer
    usable_px = 550                    # conservative container width

    total_lines = 0.0
    for segment in text.split("\n"):
        stripped = segment.strip()
        if not stripped:
            total_lines += 0.4         # blank line counts as small gap
            continue
        cjk = sum(1 for c in stripped if "\u2e80" <= c <= "\u9fff" or "\uf900" <= c <= "\ufaff")
        others = len(stripped) - cjk
        width_px = cjk * font_size + others * (font_size * 0.56)
        total_lines += max(1, (int(width_px) + usable_px - 1) // usable_px)

    display_blocks = text.count("$$") // 2
    return min(12 + int(total_lines * line_h) + display_blocks * font_size * 3, 1200)


def render_math_block(text: str, *, font_size: int = 18) -> None:
    formatted = format_math_text(text)
    html_body = escape(formatted)
    # Convert newlines to <br> but protect $$ ... $$ display math blocks,
    # because inserting <br> elements inside $$ ... $$ splits text nodes and
    # prevents MathJax from recognising the delimiters.
    parts = re.split(r"(\$\$[\s\S]*?\$\$)", html_body)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"\n{2,}", "<br>", parts[i]).replace("\n", "<br>")
    html_body = "".join(parts)
    render_height = estimate_html_height(formatted, font_size)

    html = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <script>
      // Detect dark/light by reading .stApp background; re-apply on theme change
      (function() {{
        function applyTheme() {{
          try {{
            var p = window.parent;
            var appEl = p.document.querySelector('.stApp');
            var bg = appEl ? p.getComputedStyle(appEl).backgroundColor : '';
            var m = bg.match(/(\d+),\s*(\d+),\s*(\d+)/);
            if (m) {{
              var lum = (0.299 * +m[1] + 0.587 * +m[2] + 0.114 * +m[3]) / 255;
              var dark = lum < 0.5;
              document.documentElement.style.setProperty('--text-color', dark ? '#f9fafb' : '#111827');
              document.documentElement.style.setProperty('--code-bg',   dark ? '#374151' : '#f3f4f6');
            }}
          }} catch(e) {{}}
        }}
        applyTheme();
        try {{
          // Re-apply whenever Streamlit toggles a class/attribute on <html>
          new MutationObserver(applyTheme).observe(
            window.parent.document.documentElement,
            {{ attributes: true }}
          );
        }} catch(e) {{}}
      }})();
      window.MathJax = {{
        tex: {{
          inlineMath: [['$','$'],['\\\\(','\\\\)']],
          displayMath: [['$$','$$'],['\\\\[','\\\\]']]
        }},
        svg: {{ fontCache: 'global' }}
      }};
    </script>
    <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    <style>
      :root {{ --text-color: #111827; --code-bg: #f3f4f6; }}
      * {{ box-sizing: border-box; }}
      html, body {{ margin: 0; padding: 0; overflow: hidden; }}
      body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: var(--text-color);
        background: transparent;
        font-size: {font_size}px;
        line-height: 1.5;
        word-break: break-word;
      }}
      strong {{ font-weight: 700; }}
      code {{
        background: var(--code-bg);
        color: var(--text-color);
        border-radius: 6px;
        padding: 0.1rem 0.35rem;
      }}
      ul, ol {{ margin: 0.4rem 0 0.8rem 1.2rem; padding: 0; }}
      li {{ margin: 0.25rem 0; }}
    </style>
  </head>
  <body><div>{html_body}</div></body>
</html>"""
    components.html(html, height=render_height, scrolling=False)


def init_state() -> None:
    defaults = {
        "quiz_started": False,
        "quiz_finished": False,
        "quiz_questions": [],
        "current_index": 0,
        "answers": {},
        "cheated": set(),
        "selected_count": 50,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def start_quiz() -> None:
    questions = load_questions()
    count = st.session_state.selected_count
    st.session_state.quiz_questions = random.sample(questions, count)
    st.session_state.quiz_started = True
    st.session_state.quiz_finished = False
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.cheated = set()

    for index in range(count):
        st.session_state.pop(f"answer_{index}", None)
        st.session_state.pop(f"cheat_{index}", None)


def next_question() -> None:
    current_index = st.session_state.current_index
    persist_current_question(current_index)

    if current_index + 1 >= len(st.session_state.quiz_questions):
        st.session_state.quiz_finished = True
    else:
        st.session_state.current_index += 1


def previous_question() -> None:
    current_index = st.session_state.current_index
    persist_current_question(current_index)
    if current_index > 0:
        st.session_state.current_index -= 1


def persist_current_question(index: int) -> None:
    cheat_key = f"cheat_{index}"
    if st.session_state.get(cheat_key, False):
        st.session_state.cheated.add(index)
    else:
        st.session_state.cheated.discard(index)


def restart_quiz() -> None:
    st.session_state.quiz_started = False
    st.session_state.quiz_finished = False
    st.session_state.quiz_questions = []
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.cheated = set()


def calculate_score() -> tuple[int, int]:
    score = 0
    for index, question in enumerate(st.session_state.quiz_questions):
        if index in st.session_state.cheated:
            continue
        if st.session_state.answers.get(index) == question["answer"]:
            score += POINTS_PER_QUESTION

    max_score = len(st.session_state.quiz_questions) * POINTS_PER_QUESTION
    return score, max_score


def render_quiz() -> None:
    index = st.session_state.current_index
    question = st.session_state.quiz_questions[index]
    options = {item["key"]: item["text"] for item in question["options"]}
    cheat_key = f"cheat_{index}"
    previous_answer = st.session_state.answers.get(index)

    st.progress((index + 1) / len(st.session_state.quiz_questions))
    st.caption(f"第 {index + 1} / {len(st.session_state.quiz_questions)} 題")

    render_math_block(question["question"], font_size=22)
    st.caption(f"難度：{question['difficulty']} | 來源：{question['source']}")

    option_keys = [opt["key"] for opt in question["options"]]
    selected = st.radio(
        "選項",
        options=option_keys,
        format_func=lambda k: f"{k}．{options[k]}",
        index=option_keys.index(previous_answer) if previous_answer in option_keys else None,
        label_visibility="collapsed",
    )
    if selected is not None:
        st.session_state.answers[index] = selected

    cheated = st.toggle("作弊：顯示答案與詳解（該題不計分）", key=cheat_key)
    if cheated:
        correct_option = options[question["answer"]]
        st.info(f"答案：{question['answer']}．{correct_option}")
        render_math_block(question["explanation"], font_size=18)

    previous_col, next_col = st.columns(2)
    with previous_col:
        st.button("上一題", on_click=previous_question, disabled=index == 0)
    with next_col:
        button_label = "完成測驗" if index == len(st.session_state.quiz_questions) - 1 else "下一題"
        st.button(button_label, on_click=next_question, type="primary")


def render_result() -> None:
    score, max_score = calculate_score()
    total_cheated = len(st.session_state.cheated)
    correct_count = score // POINTS_PER_QUESTION

    st.success(f"測驗完成，得分 {score} / {max_score}")
    st.write(f"答對 {correct_count} 題，共 {len(st.session_state.quiz_questions)} 題。")
    st.write(f"作弊題數：{total_cheated} 題，這些題目不列入計分。")

    st.divider()
    st.subheader("全部題目預覽")
    for index, question in enumerate(st.session_state.quiz_questions, start=1):
        user_answer = st.session_state.answers.get(index - 1)
        cheated = (index - 1) in st.session_state.cheated
        is_correct = user_answer == question["answer"] and not cheated
        status_label = "正確" if is_correct else "錯誤"
        status_color = "#15803d" if is_correct else "#dc2626"
        user_answer_label = user_answer if user_answer is not None else "未作答"

        st.markdown(
            (
                f"<div style='padding:0.9rem 1rem;border:1px solid #d1d5db;border-radius:12px;margin:0.8rem 0;'>"
                f"<div style='display:flex;justify-content:space-between;gap:1rem;align-items:center;'>"
                f"<strong>第 {index} 題｜難度：{question['difficulty']}｜來源：{question['source']}</strong>"
                f"<span style='color:white;background:{status_color};padding:0.2rem 0.6rem;border-radius:999px;'>"
                f"{status_label}</span></div></div>"
            ),
            unsafe_allow_html=True,
        )
        render_math_block(f"題目：{question['question']}", font_size=20)
        options_text = "\n".join(f"{option['key']}. {option['text']}" for option in question["options"])
        render_math_block(options_text, font_size=18)
        render_math_block(f"你的答案：{user_answer_label}", font_size=18)
        render_math_block(f"正確答案：{question['answer']}", font_size=18)
        if cheated:
            st.warning("這一題曾開啟作弊模式，因此不計分。")
        render_math_block(f"詳解：\n\n{question['explanation']}", font_size=18)
        st.divider()

    st.button(f"重新抽 {len(st.session_state.quiz_questions)} 題", on_click=restart_quiz)


def main() -> None:
    st.set_page_config(page_title=PAGE_TITLE, page_icon="🧠", layout="centered")
    init_state()

    st.title(PAGE_TITLE)
    st.write("系統會從題庫中隨機抽題，每次只顯示 1 題。")
    st.write("每題 2 分；若開啟作弊模式，會立即顯示答案與詳解，但該題不計分。")

    if not st.session_state.quiz_started:
        st.session_state.selected_count = st.radio(
            "選擇題數",
            options=[10, 30, 50],
            index=[10, 30, 50].index(st.session_state.selected_count),
            horizontal=True,
        )
        st.button("開始測驗", on_click=start_quiz, type="primary")
        return

    if st.session_state.quiz_finished:
        render_result()
        return

    render_quiz()


if __name__ == "__main__":
    main()
