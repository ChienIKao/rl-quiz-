import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "QnA.md"
OUTPUT_JSON = ROOT / "data" / "questions.json"

CHATGPT_SECTION_MAP = {
    "一、簡單題（1–15）": "簡單",
    "二、中等題（16–35）": "中等",
    "三、困難題（36–50）": "困難",
}

GEMINI_SECTION_MAP = {
    "### 一、 簡單程度 (1-15 題)": "簡單",
    "### 二、 中等程度 (16-35 題)": "中等",
    "### 三、 困難程度 (36-50 題)": "困難",
}

CLAUDE_SECTION_MAP = {
    "## 🟢 簡單（第 1–18 題）": "簡單",
    "## 🟡 中等（第 19–38 題）": "中等",
    "## 🔴 困難（第 39–50 題）": "困難",
}

MANUAL_OVERRIDES = {
    ("ChatGPT", 1): {
        "explanation": (
            "PDF 中指出，Agent 在每一步 $t$ 會先接收到環境狀態的表示 $S_t \\in S$，"
            "然後選擇一個動作 $A_t \\in A(s)$，接著才會因為該動作獲得 reward $R_{t+1}$。"
            "所以最先接收到的是 state 的表示，不是 reward。"
        ),
    },
    ("ChatGPT", 3): {
        "question": "在 return $G_t$ 的公式中，符號 $\\gamma$ 代表什麼？",
        "explanation": (
            "PDF 中的 return 公式為\n"
            "$$\n"
            "G_t = \\sum_{k=0}^{H} \\gamma^k r_{t+k+1}\n"
            "$$\n"
            "其中 $\\gamma$ 被明確稱為 discount factor，用來折扣未來的 reward。"
            "若 $\\gamma$ 越小，越不重視遠期回報；越接近 1，越重視長期回報。"
        ),
    },
    ("ChatGPT", 4): {
        "explanation": (
            "PDF 說明 MDP 是一個 5-tuple：\n"
            "$$\n"
            "(S, A, P, R, \\gamma)\n"
            "$$\n"
            "分別代表 states、actions、transition probabilities、reward、discount factor。"
            "$\\alpha$ 是 learning rate，常出現在 MC、TD、Sarsa、Q-learning 中，"
            "但不是 MDP 定義的一部分。"
        ),
    },
    ("ChatGPT", 5): {
        "question": "$V^\\pi(s)$ 代表什麼？",
        "explanation": (
            "PDF 將 value function 定義為\n"
            "$$\n"
            "V^\\pi(s) = E[G_t \\mid S_t = s]\n"
            "$$\n"
            "也就是在策略 $\\pi$ 下，從狀態 $s$ 開始並持續依照該策略行動時，"
            "所能得到的期望累積折扣 reward。它不是單一步的 reward，而是整體長期表現的估計。"
        ),
    },
    ("ChatGPT", 6): {
        "question": "$q^\\pi(s,a)$ 代表什麼？",
        "explanation": (
            "PDF 將 action-value function 定義為\n"
            "$$\n"
            "q^\\pi(s,a) = E_\\pi[G_t \\mid S_t = s, A_t = a]\n"
            "$$\n"
            "意思是：在 state $s$ 先採取 action $a$，之後再依循 policy $\\pi$ 時，"
            "所能得到的期望回報。它比 $V^\\pi(s)$ 更細，因為它把 action 也納入考慮。"
        ),
    },
    ("ChatGPT", 24): {
        "question": "在非平穩問題中，Monte Carlo 對 $V(S_t)$ 的更新式使用了哪個參數來控制遺忘舊經驗的程度？",
        "explanation": (
            "PDF 給出非平穩問題中的 MC 更新：\n"
            "$$\n"
            "V(S_t) \\leftarrow V(S_t) + \\alpha [G_t - V(S_t)]\n"
            "$$\n"
            "其中 $\\alpha$ 是 learning rate，也被說明為 "
            "\"how much we want to forget about past experiences\"。因此答案是 $\\alpha$。"
        ),
    },
    ("ChatGPT", 25): {
        "explanation": (
            "Sarsa 的更新式為\n"
            "$$\n"
            "Q(s_t,a_t) \\leftarrow Q(s_t,a_t) + \\alpha [r_t + \\gamma Q(s_{t+1}, a_{t+1}) - Q(s_t,a_t)]\n"
            "$$\n"
            "這裡的 $a_{t+1}$ 是根據當前 policy 選出的下一動作，而不是取最大值，因此它是 on-policy。"
        ),
    },
    ("ChatGPT", 27): {
        "explanation": (
            "PDF 給出 n-step return：前面累積數步 reward，最後再加上一個 "
            "$\\gamma^n Q(S_{t+n})$ 的 bootstrap 項。也就是說，它介於純 MC 和 1-step TD 之間，"
            "是多步回報與 bootstrapping 的結合。"
        ),
    },
    ("ChatGPT", 28): {
        "question": "Forward-view Sarsa($\\lambda$) 的 $q_t^\\lambda$ 是什麼？",
        "explanation": (
            "PDF 顯示\n"
            "$$\n"
            "q_t^\\lambda = (1-\\lambda) \\sum_{n=1}^{\\infty} \\lambda^{n-1} q_t^{(n)}\n"
            "$$\n"
            "表示它把不同長度的 n-step return 依照 $\\lambda$ 做加權整合，所以不是單一 return，"
            "而是多個 n-step return 的混合。"
        ),
    },
    ("ChatGPT", 29): {
        "explanation": (
            "PDF 指出 TD methods 直接從 raw experience 學習，不需要環境 model，且它用\n"
            "$$\n"
            "R_{t+1} + \\gamma V(S_{t+1})\n"
            "$$\n"
            "這種估計值來取代完整的 $G_t$。這就是 bootstrapping，也代表它不一定要等 episode 結束才更新。"
        ),
    },
    ("ChatGPT", 30): {
        "explanation": (
            "PDF 給出的 TD 更新為\n"
            "$$\n"
            "V(S_t) \\leftarrow V(S_t) + \\alpha \\bigl[R_{t+1} + \\gamma V(S_{t+1}) - V(S_t)\\bigr]\n"
            "$$\n"
            "所以它使用的目標是「當前 reward + 下一 state value 的折扣估計」，而不是完整 episode return。"
        ),
    },
    ("ChatGPT", 31): {
        "explanation": (
            "PDF 在 Q-learning 演算法中提到：Choose $a$ from $s$ using policy derived from Q "
            "(e.g., $\\epsilon$-greedy)。這表示常見的做法是用 $\\epsilon$-greedy 來平衡 "
            "exploration 與 exploitation。"
        ),
    },
    ("ChatGPT", 32): {
        "question": "$\\epsilon$-greedy 中，$\\epsilon$ 的作用是什麼？",
        "explanation": (
            "在 $\\epsilon$-greedy 中，大部分時間選目前估計最好的 action，但有機率 $\\epsilon$ "
            "隨機探索其他 action。這樣可避免過早陷入局部最佳。"
        ),
    },
    ("ChatGPT", 33): {
        "question": "Deep Q Learning 的 loss $L_i(\\theta_i)$ 中，prediction 是什麼？",
    },
    ("ChatGPT", 34): {
        "explanation": (
            "從 PDF 的 target 可看出，非 terminal 狀態時\n"
            "$$\n"
            "y_j = r_j + \\gamma \\max_a Q(s'_j,a';\\theta)\n"
            "$$\n"
            "因此它由即時 reward 和未來最佳 Q 值的折扣部分組成。若是 terminal state，則只有 $r_j$。"
        ),
    },
    ("ChatGPT", 35): {
        "question": "在 DQL 中，若 $s'_j$ 是 terminal state，則 $y_j$ 應設為何？",
        "explanation": (
            "PDF 在演算法裡明確寫到：\n"
            "- terminal $s'_j$：$y_j = r_j$\n"
            "- non-terminal $s'_j$：$y_j = r_j + \\gamma \\max_a Q(s'_j,a')$\n"
            "因為終止狀態之後沒有未來回報，所以 target 只剩下當前 reward。"
        ),
    },
    ("ChatGPT", 41): {
        "explanation": (
            "TD 的更新式中含有 $V(S_{t+1})$ 或 $Q(s',a')$ 這類「目前估計值」，"
            "表示它用自己的估計輔助更新自己，這就是 bootstrapping。與 MC 使用完整 sample return 相比，"
            "TD 更早更新，但也引入估計誤差來源。"
        ),
    },
    ("ChatGPT", 44): {
        "question": "在 Forward-view Sarsa($\\lambda$) 中，$\\lambda$ 的功能最接近下列何者？",
    },
    ("Gemini", 14): {
        "question": "$G_t = \\sum_{k=0}^{H}\\gamma^{k}r_{t+k+1}$ 中，$H$ 代表？",
    },
    ("Gemini", 16): {
        "question": "狀態轉移機率 $p(s'|s,a)$ 代表的意義是？",
        "explanation": "這是轉移機率的定義：$Pr\\{S_{t+1}=s' \\mid S_t=s, A_t=a\\}$。",
    },
    ("Gemini", 17): {
        "question": "動作價值函數 $q_\\pi(s,a)$ 與狀態價值函數 $V_\\pi(s)$ 的主要區別在於？",
    },
    ("Gemini", 23): {
        "question": (
            "Sarsa 更新規則 "
            "$Q(s_t,a_t) \\leftarrow Q(s_t,a_t) + \\alpha[r_t + \\gamma Q(s_{t+1},a_{t+1}) - Q(s_t,a_t)]$ "
            "表現了什麼？"
        ),
        "explanation": (
            "Sarsa 使用 $Q(s_{t+1}, a_{t+1})$，也就是當前策略實際選出的下一個動作對應的值來更新。"
        ),
    },
    ("Gemini", 34): {
        "question": "在時序差分學習中，$V(S_t)$ 的更新朝向哪個目標？",
        "options": [
            {"key": "A", "text": "$G_t$"},
            {"key": "B", "text": "$R_{t+1} + \\gamma V(S_{t+1})$"},
            {"key": "C", "text": "$V(S_{t-1})$"},
            {"key": "D", "text": "$\\arg\\max_a Q(s, a)$"},
        ],
        "explanation": "TD 更新是朝向 TD 目標 $R_{t+1} + \\gamma V(S_{t+1})$。",
    },
    ("Gemini", 29): {
        "question": "如果 $H$（Horizon）是無限的，為了保證總回報 $G_t$ 收斂，$\\gamma$ 必須滿足？",
    },
    ("Gemini", 38): {
        "question": "Forward View Sarsa($\\lambda$) 的權重項 $(1-\\lambda)\\lambda^{n-1}$ 作用為何？",
        "explanation": "這是 $\\lambda$-return 的定義，整合了所有 $n$-step 的回報。",
    },
    ("Gemini", 39): {
        "question": "DQL 的 Loss Function $L_i(\\theta_i)$ 中，為什麼 $\\theta_{i-1}$ 要加下標 $i-1$？",
    },
    ("Gemini", 41): {
        "question": "在蒙地卡羅方法更新式 $V(S_t) \\leftarrow V(S_t) + \\alpha [G_t - V(S_t)]$ 中，$[G_t - V(S_t)]$ 被稱為什麼？",
    },
    ("Gemini", 47): {
        "question": "在 DQL 中，若 $s'_j$ 是終止狀態（Terminal State），其目標值 $y_j$ 應設為？",
    },
    ("Gemini", 48): {
        "question": "貝爾曼方程展示了 $q_\\pi(s,a)$ 可以用 $V_\\pi(s')$ 來表示，其關係式為？",
    },
    ("Claude", 1): {
        "question": "在 Agent-Environment Interface 中，Agent 在時間步 $t$ 採取動作 $A_t$ 後，環境會回傳什麼？",
        "explanation": (
            "根據 Agent-Environment Interface，Agent 在每個時間步 $t$ 觀察到狀態 $S_t$，"
            "並選擇動作 $A_t$，環境隨後回傳下一狀態 $S_{t+1}$ 與獎勵 $R_{t+1}$。"
        ),
    },
    ("Claude", 41): {
        "question": "在 Sarsa($\\lambda$) 中，$\\lambda$ 的值如何影響算法行為？請分析 $\\lambda = 0$ 和 $\\lambda = 1$ 的極端情況。",
        "explanation": (
            "分析 Forward View Sarsa($\\lambda$)：\n"
            "$$\n"
            "q_t^\\lambda = (1-\\lambda) \\sum_{n=1}^{\\infty} \\lambda^{n-1} q_t^{(n)}\n"
            "$$\n"
            "- **$\\lambda = 0$**：$q_t^\\lambda = q_t^{(1)}$，也就是只有 1-step return，退化為 TD(0)，即普通 SARSA。\n"
            "- **$\\lambda = 1$**：在有限 episode 中可視為完整的 Monte Carlo return。\n"
            "- 中間值的 $\\lambda$ 會在 TD 和 MC 之間做插值。"
        ),
    },
    ("Claude", 42): {
        "question": "為什麼 DQN 使用過去的參數 $\\theta_{i-1}$ 作為 Target，而不是當前參數 $\\theta_i$？",
        "explanation": (
            "若 Target 和 Prediction 使用相同參數，更新 $\\theta$ 時會同時改變 Target 值，"
            "造成 moving target 問題，讓訓練非常不穩定。DQN 使用固定一段時間的 "
            "$\\theta_{i-1}$ 作為 Target，可讓學習訊號更穩定。"
        ),
    },
    ("Claude", 46): {
        "explanation": (
            "MDP 的核心是 **Markov Property**："
            "$Pr\\{S_{t+1} = s' \\mid S_t, A_t, S_{t-1}, A_{t-1}, \\ldots\\} = "
            "Pr\\{S_{t+1} = s' \\mid S_t, A_t\\}$。"
            "即給定當前狀態 $S_t$ 和動作 $A_t$，過去的歷史不提供任何額外資訊。"
            "若環境不滿足 Markov 性質，則需要用 POMDP 等延伸框架。"
        ),
    },
    ("Claude", 43): {
        "explanation": (
            "當 $\\gamma = 1$ 且 $H = \\infty$ 時，$G_t = \\sum_{k=0}^{\\infty} r_{t+k+1}$ 可能發散。"
            "Bellman Equation 的收斂性依賴 $\\gamma < 1$ 或有限 horizon $H < \\infty$。"
            "當 $\\gamma < 1$ 時，幾何級數 $\\sum_{k=0}^{\\infty} \\gamma^k = \\frac{1}{1-\\gamma}$ 才會收斂。"
        ),
    },
    ("Claude", 44): {
        "explanation": (
            "這是經典的 Cliff Walking 例子。Q-Learning 學習的是最優策略的 Q 值"
            "（使用 $\\max_{a'}$），不考慮當前 $\\epsilon$-greedy 策略的隨機性，因此會偏向懸崖邊的最短路徑。"
            "SARSA 會把 $\\epsilon$-greedy 的探索風險也考慮進去，所以通常學到更保守、較安全的路徑。"
        ),
    },
    ("Claude", 47): {
        "question": "在 n-step SARSA 中，若 $n=1$ 和 $n=\\infty$ 分別對應什麼方法？$n$ 的選擇如何影響 Bias-Variance Tradeoff？",
        "options": [
            {"key": "A", "text": "$n=1$ 對應 MC；$n=\\infty$ 對應 TD；較大的 $n$ 降低 Bias 但增加 Variance"},
            {"key": "B", "text": "$n=1$ 對應 TD(SARSA)；$n=\\infty$ 對應 MC；較大的 $n$ 降低 Bias 但增加 Variance"},
            {"key": "C", "text": "$n=1$ 對應 TD(SARSA)；$n=\\infty$ 對應 MC；較大的 $n$ 降低 Variance 但增加 Bias"},
            {"key": "D", "text": "$n$ 的大小不影響 Bias-Variance Tradeoff"},
        ],
        "explanation": (
            "n-step Q-return 為\n"
            "$$\n"
            "q_t^{(n)} = R_{t+1} + \\gamma R_{t+2} + \\cdots + \\gamma^{n-1} R_{t+n} + \\gamma^n Q(S_{t+n})\n"
            "$$\n"
            "- $n=1$ 時，退化為 1-step TD，也就是 SARSA。\n"
            "- $n=\\infty$ 時，退化為 Monte Carlo。\n"
            "較大的 $n$ 通常會降低 Bias，但提高 Variance。"
        ),
    },
    ("Claude", 48): {
        "explanation": (
            "標準 DQN 的 target 為 $r + \\gamma \\max_{a'} Q(s', a'; \\theta_{i-1})$，"
            "會用同一個估計同時做動作選擇與價值評估，因此容易高估。"
            "Double DQN 的改進是：先用當前網路選出 "
            "$a^* = \\arg\\max_a Q(s', a; \\theta)$，再用 target network 評估 $Q(s', a^*; \\theta')$，"
            "藉此降低 overestimation。"
        ),
    },
    ("Claude", 49): {
        "explanation": (
            "定義 Bellman optimality operator 為 "
            "$(TV)(s) = \\max_a \\sum_{s',r} p(s',r|s,a)[r + \\gamma V(s')]$。"
            "當 $\\gamma < 1$ 時，$T$ 在 $\\sup$-norm 下是 contraction mapping："
            "$\\|TV - TU\\|_\\infty \\leq \\gamma \\|V-U\\|_\\infty$。"
            "因此依 Banach fixed-point theorem，$T$ 有唯一不動點，也就是 $V^*$。"
        ),
    },
    ("Claude", 50): {
        "explanation": (
            "三大方法的完整對比：\n\n"
            "| 方法 | 需要環境模型 | 需要完整 Episode | 使用 Bootstrap |\n"
            "|---|---|---|---|\n"
            "| DP | 是 | 否 | 是 |\n"
            "| MC | 否 | 是 | 否 |\n"
            "| TD | 否 | 否 | 是 |\n\n"
            "Bootstrap 指用目前的 value estimate 來更新自己，而不是等完整真實回報。"
        ),
    },
}

EXTRA_OVERRIDES = {
    ("ChatGPT", 17): {
        "explanation": "當 $\\gamma$ 越大，未來 reward 被折扣得越少，因此長期回報對目前決策的影響越大。反之，若 $\\gamma$ 很小，Agent 會偏向短視近利，只重視近期 reward。",
    },
    ("ChatGPT", 43): {
        "explanation": "n-step Sarsa 前面累積多步實際 reward，但最後仍接一個 bootstrap 的 $Q(S_{t+n})$ 項。因此它不像 1-step TD 那麼短視，也不像 MC 那樣要等完整 episode，正好處於兩者之間。",
    },
    ("ChatGPT", 44): {
        "explanation": "PDF 給出 $$q_t^\\lambda = (1-\\lambda)\\sum_{n=1}^{\\infty}\\lambda^{n-1}q_t^{(n)}$$，由這個式子可看出，$\\lambda$ 是用來調整不同 n-step returns 權重的參數。它不是 discount factor，discount factor 是 $\\gamma$。",
    },
    ("ChatGPT", 49): {
        "explanation": "PDF 在 DQL 演算法中寫道：以機率 $\\epsilon$ 隨機選 action，否則選擇 $a = \\max_a Q(s,a;\\theta)$。這就是 $\\epsilon$-greedy 的標準定義。",
    },
    ("Gemini", 1): {
        "explanation": "代理人在每一步 $t$ 接收環境狀態的表徵 $S_t \\in S$。",
    },
    ("Gemini", 4): {
        "explanation": "在 $G_t$ 的計算中，$\\gamma$ 是折扣因子。",
    },
    ("Gemini", 13): {
        "explanation": "$S$ 代表有限的狀態集合，且 $s \\in S$。",
    },
    ("Gemini", 30): {
        "explanation": "$n$-step Q-Return 包含 $n$ 步獎勵的折扣和，以及最後的 bootstrap 項 $Q(S_{t+n})$。",
    },
    ("Gemini", 43): {
        "explanation": "以機率 $\\epsilon$ 進行隨機探索，否則選擇使 $Q$ 值最大的動作。",
    },
    ("Claude", 2): {
        "explanation": "Policy 是從狀態到動作的映射，$\\pi_t(s|a)$ 表示在狀態 $S_t=s$ 時，選擇動作 $A_t=a$ 的機率。",
    },
    ("Claude", 3): {
        "explanation": "$\\gamma$ 為折扣因子（Discount Factor），範圍通常為 $[0,1]$。它控制未來獎勵相對於即時獎勵的重要性。",
    },
    ("Claude", 4): {
        "explanation": "MDP 是一個 5-tuple：$$(S, A, P, R, \\gamma)$$ 其中 $S$ 為狀態集合，$A$ 為動作集合，$P$ 為狀態轉移機率，$R$ 為獎勵函數，$\\gamma$ 為折扣因子。",
    },
    ("Claude", 5): {
        "explanation": "狀態轉移機率表示在狀態 $s$ 執行動作 $a$ 後，轉移到狀態 $s'$ 的機率，也就是 $p(s'|s,a)$。",
    },
    ("Claude", 6): {
        "explanation": "$V_\\pi(s)=E[G_t|S_t=s]$，代表從狀態 $s$ 出發並遵循策略 $\\pi$ 的預期累積折扣獎勵。",
    },
    ("Claude", 8): {
        "explanation": "$q_\\pi(s,a)=E_\\pi[G_t|S_t=s,A_t=a]$，表示在狀態 $s$ 執行動作 $a$，之後遵循策略 $\\pi$ 時的預期回報。",
    },
    ("Claude", 10): {
        "explanation": "Policy Iteration 初始化時會令 $\\Delta \\leftarrow 0$，用來追蹤 value function 的最大更新量。",
    },
    ("Claude", 11): {
        "explanation": "Policy Evaluation 會持續進行，直到 $\\Delta < \\theta$ 為止。",
    },
    ("Claude", 14): {
        "explanation": "非穩態問題中的 Monte Carlo 更新為 $V(S_t) \\leftarrow V(S_t) + \\alpha [G_t - V(S_t)]$，其中 $\\alpha$ 控制對新資訊的信任程度。",
    },
    ("Claude", 16): {
        "explanation": "SARSA 是 on-policy 方法，因為更新時使用的 $a_{t+1}$ 是策略 $\\pi$ 實際選出的下一個動作。",
    },
    ("Claude", 18): {
        "explanation": "TD 更新公式為 $V(S_t) \\leftarrow V(S_t) + \\alpha [R_{t+1} + \\gamma V(S_{t+1}) - V(S_t)]$。",
    },
    ("Claude", 19): {
        "explanation": "Bellman Equation（Value Function）為 $$V_\\pi(s)=\\sum_a \\pi(a|s)\\sum_{s',r}p(s',r|s,a)[r+\\gamma V_\\pi(s')]$$ 其中要對所有動作依照 $\\pi(a|s)$ 加權。",
    },
    ("Claude", 20): {
        "explanation": "Q Function 的 Bellman 方程式為 $$q_\\pi(s,a)=\\sum_{s',r}p(s',r|s,a)[r+\\gamma V_\\pi(s')]$$，由於動作 $a$ 已經固定，因此不需要再對 $\\pi(a|s)$ 加權。",
    },
    ("Claude", 24): {
        "explanation": "Value Iteration 的更新式為 $$V(s) \\leftarrow \\max_a \\sum_{s',r} p(s',r|s,a)[r+\\gamma V(s')]$$，它直接取最大值，因此同時帶有 policy improvement 的效果。",
    },
    ("Claude", 25): {
        "explanation": "SARSA 的更新規則為 $Q(s_t,a_t) \\leftarrow Q(s_t,a_t)+\\alpha[r_t+\\gamma Q(s_{t+1},a_{t+1})-Q(s_t,a_t)]$，關鍵是使用實際執行的下一個動作 $a_{t+1}$。",
    },
    ("Claude", 26): {
        "explanation": "Q-Learning 使用 $\\max_{a'}Q(s',a')$，與當前策略無關，因此是 off-policy；SARSA 使用實際選出的 $a'$，因此是 on-policy。",
    },
    ("Claude", 27): {
        "explanation": "n-step Q-Return 的定義為 $q_t^{(n)} = R_{t+1}+\\gamma R_{t+2}+\\cdots+\\gamma^{n-1}R_{t+n}+\\gamma^nQ(S_{t+n})$。",
    },
    ("Claude", 28): {
        "question": "Forward View Sarsa($\\lambda$) 的 $q_t^\\lambda$ 定義是？",
        "options": [
            {"key": "A", "text": "$q_t^\\lambda = \\lambda \\sum_{n=1}^{\\infty} (1-\\lambda)^{n-1} q_t^{(n)}$"},
            {"key": "B", "text": "$q_t^\\lambda = (1-\\lambda) \\sum_{n=1}^{\\infty} \\lambda^{n-1} q_t^{(n)}$"},
            {"key": "C", "text": "$q_t^\\lambda = \\sum_{n=1}^{\\infty} \\lambda^n q_t^{(n)}$"},
            {"key": "D", "text": "$q_t^\\lambda = (1-\\lambda) q_t^{(1)} + \\lambda q_t^{(\\infty)}$"},
        ],
        "explanation": "Forward View Sarsa($\\lambda$) 的 $\\lambda$-return 為 $q_t^\\lambda=(1-\\lambda)\\sum_{n=1}^{\\infty}\\lambda^{n-1}q_t^{(n)}$。",
    },
    ("Claude", 29): {
        "question": "Deep Q-Learning（DQN）的損失函數 $L_i(\\theta_i)$ 中，Target 的計算方式是？",
        "explanation": "DQN 的 loss 中，target 會使用 $r + \\gamma \\max_{a'} Q(s', a'; \\theta_{i-1})$，也就是上一版或 target network 的估計。",
    },
    ("Claude", 30): {
        "explanation": "Experience Replay 會把 transition $(s,a,r,s')$ 存入 replay memory $D$，訓練時再從中隨機取樣 minibatch。",
    },
    ("Claude", 31): {
        "explanation": "$\\epsilon$-greedy 表示以機率 $\\epsilon$ 隨機選動作，以機率 $1-\\epsilon$ 選擇使 $Q(s,a;\\theta)$ 最大的動作。",
    },
    ("Claude", 32): {
        "explanation": "Policy Evaluation 在固定策略 $\\pi$ 下使用 Bellman expectation equation 來更新 $V(s)$。",
    },
    ("Claude", 34): {
        "question": "Sarsa($\\lambda$) 演算法（Algorithm 4）中，使用的策略是哪種？",
        "explanation": "Sarsa($\\lambda$) 演算法中常用由 Q 導出的 $\\epsilon$-greedy 策略。",
    },
    ("Claude", 35): {
        "explanation": "Monte Carlo First-visit 會取每個 episode 中 $(s,a)$ 第一次出現後的 return $G$，再對 $\\mathrm{Returns}(s,a)$ 做平均來估計 $Q(s,a)$。",
    },
    ("Claude", 37): {
        "explanation": "Monte Carlo 需要等完整 episode 才能得到 $G_t$；TD 則使用 $R_{t+1}+\\gamma V(S_{t+1})$，因此可以每一步即時更新。",
    },
    ("Claude", 38): {
        "explanation": "若 $s'_j$ 是 terminal state，則 DQN 的目標值直接設為 $y_j = r_j$。",
    },
}


def normalize_text(text: str) -> str:
    text = text.replace("[cite_start]", "")
    text = re.sub(r"\s+\[cite:[^\]]+\]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def standardize_math_text(text: str) -> str:
    text = normalize_text(text)

    text = re.sub(
        r"(?ms)^\[\s*\n(.*?)\n\]$",
        lambda match: f"$$\n{match.group(1).strip()}\n$$",
        text,
    )
    text = re.sub(
        r"(?ms)\n\[\s*\n(.*?)\n\]",
        lambda match: f"\n\n$$\n{match.group(1).strip()}\n$$\n",
        text,
    )
    text = text.replace(r"\bigl[", "[").replace(r"\bigr]", "]")

    for _ in range(5):
        text = re.sub(
            r"\$([^$]*[\u4e00-\u9fff][^$]*)\(([^$]*[\u4e00-\u9fff][^$]*)\)([^$]*)\$",
            lambda match: f"${match.group(1).strip()}${match.group(2)}${match.group(3).strip()}$",
            text,
        )
    text = re.sub(
        r"([A-Za-z][A-Za-z0-9_^{}]*)\$([A-Za-z0-9\\_^{},|'+\-*/]+)\$",
        lambda match: f"{match.group(1)}({match.group(2).strip()})",
        text,
    )

    text = re.sub(
        r"\(\s*([A-Za-z0-9\\_^{},|=+\-*/' ]{1,120})\s*\)",
        lambda match: f"${match.group(1).strip()}$"
        if any(token in match.group(1) for token in ("\\", "_", "^", "="))
        else match.group(0),
        text,
    )
    text = re.sub(
        r"\(\s*(\\[A-Za-z]+(?:\([^)]+\))?)\s*\)",
        lambda match: f"${match.group(1).strip()}$",
        text,
    )
    text = re.sub(
        r"\(\s*([A-Za-z][A-Za-z0-9_^{}]*(?:\([^)]+\))?)\s*\)",
        lambda match: f"${match.group(1).strip()}$"
        if any(token in match.group(1) for token in ("_", "^"))
        else match.group(0),
        text,
    )
    text = re.sub(r"\$\s*([^$]+?)\s*\$", lambda match: f"${match.group(1).strip()}$", text)
    text = re.sub(r"\$\$\s*(.+?)\s*\$\$", lambda match: f"$$\n{match.group(1).strip()}\n$$", text, flags=re.S)
    text = re.sub(r"(?s)\$\$\n?(.*?)\n?\$\$(?=\S)", lambda match: f"$$\n{match.group(1).strip()}\n$$\n", text)
    text = re.sub(r"(?m)^\*\s+(target|prediction)：", r"- \1：", text)
    text = re.sub(r"(?m)^\*\s+(terminal|non-terminal)", r"- \1", text)
    return text.strip()


def normalize_explanation(text: str) -> str:
    lines = [line.rstrip() for line in standardize_math_text(text).splitlines()]
    cleaned: list[str] = []

    for line in lines:
        if not line and cleaned and not cleaned[-1]:
            continue
        cleaned.append(line)

    return "\n".join(cleaned).strip()


def normalize_option_text(text: str) -> str:
    return standardize_math_text(text).replace("  ", " ").strip()


def build_question(
    source: str,
    source_number: int,
    difficulty: str,
    question: str,
    options: list[dict],
    answer: str,
    explanation: str,
) -> dict:
    return {
        "source": source,
        "source_question_no": source_number,
        "difficulty": difficulty,
        "question": standardize_math_text(question),
        "options": options,
        "answer": answer.strip(),
        "explanation": normalize_explanation(explanation),
    }


def load_existing_questions() -> list[dict]:
    questions = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
    normalized = []
    for item in questions:
        normalized.append(
            {
                "source": item["source"],
                "source_question_no": item["source_question_no"],
                "difficulty": item["difficulty"],
                "question": standardize_math_text(item["question"]),
                "options": [
                    {
                        "key": option["key"],
                        "text": normalize_option_text(option["text"]),
                    }
                    for option in item["options"]
                ],
                "answer": item["answer"].strip(),
                "explanation": normalize_explanation(item["explanation"]),
            }
        )
    return normalized


def parse_chatgpt(text: str) -> list[dict]:
    questions = []
    current_difficulty = None
    lines = text.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index].strip()

        if line.startswith("## "):
            current_difficulty = CHATGPT_SECTION_MAP.get(line.replace("## ", "").strip(), current_difficulty)
            index += 1
            continue

        question_match = re.match(r"###\s*(\d+)\.\s*(.+)", line)
        if not question_match:
            index += 1
            continue

        source_number = int(question_match.group(1))
        question = question_match.group(2).strip()
        index += 1

        while index < len(lines) and not lines[index].strip():
            index += 1

        options = []
        while index < len(lines):
            option_line = lines[index].strip()
            option_match = re.match(r"(?P<key>[A-D])\.\s*(?P<content>.+)", option_line)
            if not option_match:
                break
            options.append(
                {
                    "key": option_match.group("key"),
                    "text": normalize_option_text(option_match.group("content")),
                }
            )
            index += 1

        while index < len(lines) and not lines[index].strip():
            index += 1

        answer_line = lines[index].strip() if index < len(lines) else ""
        answer_match = re.match(r"\*\*答案：(?P<answer>[A-D])\*\*", answer_line)
        if not answer_match:
            index += 1
            continue
        answer = answer_match.group("answer")
        index += 1

        while index < len(lines) and not lines[index].strip():
            index += 1

        if index < len(lines) and lines[index].strip() == "**詳解：**":
            index += 1

        explanation_parts = []
        while index < len(lines):
            current_line = lines[index].strip()
            if current_line == "---" or re.match(r"###\s*\d+\.", current_line) or current_line.startswith("## "):
                break
            explanation_parts.append(current_line)
            index += 1

        questions.append(
            build_question(
                source="ChatGPT",
                source_number=source_number,
                difficulty=current_difficulty,
                question=question,
                options=options,
                answer=answer,
                explanation="\n".join(explanation_parts),
            )
        )

        while index < len(lines) and lines[index].strip() == "---":
            index += 1

    return questions


def parse_gemini(text: str) -> list[dict]:
    questions = []
    current_difficulty = None
    lines = text.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        if line in GEMINI_SECTION_MAP:
            current_difficulty = GEMINI_SECTION_MAP[line]
            index += 1
            continue

        question_match = re.match(r"\*\*(\d+)\.\s*(.+?)\*\*(?:\s*\[cite:[^\]]+\])?$", line)
        if not question_match:
            index += 1
            continue

        source_number = int(question_match.group(1))
        question = question_match.group(2)
        index += 1

        options = []
        while index < len(lines):
            option_line = lines[index].strip()
            option_match = re.match(r"\((?P<key>[A-D])\)\s*(?P<content>.+)", option_line)
            if not option_match:
                break
            options.append(
                {
                    "key": option_match.group("key"),
                    "text": normalize_option_text(option_match.group("content")),
                }
            )
            index += 1

        while index < len(lines) and not lines[index].strip():
            index += 1

        answer_line = lines[index].strip() if index < len(lines) else ""
        answer_match = re.match(r"\*\*答案：\((?P<answer>[A-D])\)\*\*", answer_line)
        if not answer_match:
            index += 1
            continue
        answer = answer_match.group("answer")
        index += 1

        explanation_parts = []
        while index < len(lines):
            current_line = lines[index].strip()
            if (
                re.match(r"\*\*\d+\.\s*.+\*\*(?:\s*\[cite:[^\]]+\])?$", current_line)
                or current_line == "---"
                or current_line.startswith("### ")
            ):
                break
            explanation_parts.append(current_line)
            index += 1

        explanation = "\n".join(explanation_parts)
        explanation = re.sub(r"^\*\*解析：\*\*\s*", "", normalize_text(explanation))
        explanation = re.sub(r"^\*\*詳解：\*\*\s*", "", explanation)

        questions.append(
            build_question(
                source="Gemini",
                source_number=source_number,
                difficulty=current_difficulty,
                question=question,
                options=options,
                answer=answer,
                explanation=explanation,
            )
        )

        while index < len(lines) and not lines[index].strip():
            index += 1

    return questions


def parse_claude(text: str) -> list[dict]:
    questions = []
    current_difficulty = None
    lines = text.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        section_line = lines[index].strip()
        if section_line in CLAUDE_SECTION_MAP:
            current_difficulty = CLAUDE_SECTION_MAP[section_line]
            index += 1
            continue

        question_match = re.match(r"\*\*(\d+)\.\*\*\s*(.+)", line)
        if not question_match:
            index += 1
            continue

        source_number = int(question_match.group(1))
        question = question_match.group(2).strip()
        index += 1

        while index < len(lines) and not lines[index].strip():
            index += 1

        options = []
        while index < len(lines):
            option_line = lines[index].strip()
            option_match = re.match(r"- (?P<key>[A-D])\.\s*(?P<content>.+)", option_line)
            if not option_match:
                break
            options.append(
                {
                    "key": option_match.group("key"),
                    "text": normalize_option_text(option_match.group("content")),
                }
            )
            index += 1

        while index < len(lines) and not lines[index].strip():
            index += 1

        answer_line = lines[index].strip() if index < len(lines) else ""
        answer_match = re.match(r"\*\*答案：(?P<answer>[A-D])\*\*", answer_line)
        if not answer_match:
            index += 1
            continue
        answer = answer_match.group("answer")
        index += 1

        explanation_parts = []
        while index < len(lines):
            current_line = lines[index].strip()
            if (
                re.match(r"\*\*\d+\.\*\*\s*.+", current_line)
                or current_line == "---"
                or current_line.startswith("## ")
            ):
                break
            explanation_parts.append(current_line)
            index += 1

        explanation = "\n".join(explanation_parts)
        explanation = re.sub(r"^\*\*詳解：\*\*\s*", "", normalize_text(explanation))

        questions.append(
            build_question(
                source="Claude",
                source_number=source_number,
                difficulty=current_difficulty,
                question=question,
                options=options,
                answer=answer,
                explanation=explanation,
            )
        )

        while index < len(lines) and not lines[index].strip():
            index += 1

    return questions


def validate_questions(questions: list[dict]) -> None:
    if len(questions) != 150:
        raise ValueError(f"預期解析出 150 題，實際得到 {len(questions)} 題。")

    for question in questions:
        if question["difficulty"] not in {"簡單", "中等", "困難"}:
            raise ValueError(f"題目難度缺失：{question}")
        if len(question["options"]) != 4:
            raise ValueError(f"選項數量異常：{question['source']} #{question['source_question_no']}")


def assign_ids(questions: list[dict]) -> list[dict]:
    output = []
    for index, question in enumerate(questions, start=1):
        item = dict(question)
        item["id"] = index
        output.append(item)
    return output


def apply_manual_overrides(questions: list[dict]) -> list[dict]:
    output = []
    for question in questions:
        item = dict(question)
        override = MANUAL_OVERRIDES.get((item["source"], item["source_question_no"]))
        extra_override = EXTRA_OVERRIDES.get((item["source"], item["source_question_no"]))
        if override:
            for key, value in override.items():
                item[key] = value
        if extra_override:
            for key, value in extra_override.items():
                item[key] = value
        output.append(item)
    return output


def render_markdown(questions: list[dict]) -> str:
    lines = [
        "# 強化學習題庫（共 150 題）",
        "",
        "這份題庫已整理為統一格式，來源包含 ChatGPT、Gemini、Claude 三份版本，並同步產生 `questions.json` 供 Streamlit 測驗 app 使用。",
        "",
    ]

    for source in ("ChatGPT", "Gemini", "Claude"):
        lines.append(f"## {source}")
        lines.append("")

        for difficulty in ("簡單", "中等", "困難"):
            source_questions = [
                question
                for question in questions
                if question["source"] == source and question["difficulty"] == difficulty
            ]
            if not source_questions:
                continue

            lines.append(f"### {difficulty}")
            lines.append("")

            for question in source_questions:
                lines.append(
                    f"#### {question['id']}. {question['question']} "
                    f"（來源題號：{question['source_question_no']}）"
                )
                lines.append("")
                for option in question["options"]:
                    lines.append(f"- {option['key']}. {option['text']}")
                lines.append("")
                lines.append(f"**答案：{question['answer']}**")
                lines.append("")
                lines.append("**詳解：**")
                lines.append(question["explanation"])
                lines.append("")
                lines.append("---")
                lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")

    if "\n# Gemini\n" in text and "\n# Claude\n" in text:
        chatgpt_text, remainder = text.split("\n# Gemini\n", 1)
        gemini_text, claude_text = remainder.split("\n# Claude\n", 1)

        questions = []
        questions.extend(parse_chatgpt(chatgpt_text))
        questions.extend(parse_gemini(gemini_text))
        questions.extend(parse_claude(claude_text))
    elif OUTPUT_JSON.exists():
        questions = load_existing_questions()
    else:
        raise ValueError("找不到可用的原始題庫格式，也沒有現成的 questions.json。")

    questions = apply_manual_overrides(questions)
    validate_questions(questions)
    questions = assign_ids(questions)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    SOURCE.write_text(render_markdown(questions), encoding="utf-8")


if __name__ == "__main__":
    main()
