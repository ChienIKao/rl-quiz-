# 強化學習題庫（共 150 題）

這份題庫已整理為統一格式，來源包含 ChatGPT、Gemini、Claude 三份版本，並同步產生 `questions.json` 供 Streamlit 測驗 app 使用。

## ChatGPT

### 簡單

#### 1. 在強化學習的 Agent-Environment Interface 中，Agent 在每個時間步首先會接收到什麼？ （來源題號：1）

- A. Reward
- B. State 的表示
- C. 最佳 policy
- D. Q 值表

**答案：B**

**詳解：**
PDF 中指出，Agent 在每一步 $t$ 會先接收到環境狀態的表示 $S_t \in S$，然後選擇一個動作 $A_t \in A(s)$，接著才會因為該動作獲得 reward $R_{t+1}$。所以最先接收到的是 state 的表示，不是 reward。

---

#### 2. Policy 的意義最接近下列何者？ （來源題號：2）

- A. 從 state 到 action 的對應規則
- B. 從 reward 到 state 的函數
- C. 從 action 到 state 的轉移機率
- D. 從 state 到 reward 的折扣函數

**答案：A**

**詳解：**
PDF 將 policy 定義為 state 到 action 的 mapping，寫成 $\pi(a|s)$，表示在狀態 ( s ) 下選擇動作 ( a ) 的機率。因此 policy 描述的是「遇到某個 state 時要如何選 action」。

---

#### 3. 在 return $G_t$ 的公式中，符號 $\gamma$ 代表什麼？ （來源題號：3）

- A. Learning rate
- B. Horizon
- C. Discount factor
- D. Transition probability

**答案：C**

**詳解：**
PDF 中的 return 公式為
$$
G_t = \sum_{k=0}^{H} \gamma^k r_{t+k+1}
$$
其中 $\gamma$ 被明確稱為 discount factor，用來折扣未來的 reward。若 $\gamma$ 越小，越不重視遠期回報；越接近 1，越重視長期回報。

---

#### 4. 下列何者**不是** MDP 的組成元素？ （來源題號：4）

- A. ( S )
- B. ( A )
- C. ( P )
- D. $\alpha$

**答案：D**

**詳解：**
PDF 說明 MDP 是一個 5-tuple：
$$
(S, A, P, R, \gamma)
$$
分別代表 states、actions、transition probabilities、reward、discount factor。$\alpha$ 是 learning rate，常出現在 MC、TD、Sarsa、Q-learning 中，但不是 MDP 定義的一部分。

---

#### 5. $V^\pi(s)$ 代表什麼？ （來源題號：5）

- A. 在 state ( s ) 下立即得到的 reward
- B. 在 policy $\pi$ 下，從 state ( s ) 出發的期望累積折扣回報
- C. 在 state ( s ) 下所有 action 的平均 reward
- D. 從 state ( s ) 轉移到下一狀態的機率

**答案：B**

**詳解：**
PDF 將 value function 定義為
$$
V^\pi(s) = E[G_t \mid S_t = s]
$$
也就是在策略 $\pi$ 下，從狀態 $s$ 開始並持續依照該策略行動時，所能得到的期望累積折扣 reward。它不是單一步的 reward，而是整體長期表現的估計。

---

#### 6. $q^\pi(s,a)$ 代表什麼？ （來源題號：6）

- A. 在 state-action 配對下的期望回報
- B. 在 state ( s ) 的轉移機率
- C. 最佳 policy
- D. 折扣因子

**答案：A**

**詳解：**
PDF 將 action-value function 定義為
$$
q^\pi(s,a) = E_\pi[G_t \mid S_t = s, A_t = a]
$$
意思是：在 state $s$ 先採取 action $a$，之後再依循 policy $\pi$ 時，所能得到的期望回報。它比 $V^\pi(s)$ 更細，因為它把 action 也納入考慮。

---

#### 7. 最佳 value function ( V^*(s) ) 的定義為何？ （來源題號：7）

- A. ( \min_\pi V^\pi(s) )
- B. ( \max_\pi V^\pi(s) )
- C. ( \sum_\pi V^\pi(s) )
- D. ( V^\pi(s) - q^\pi(s,a) )

**答案：B**

**詳解：**
PDF 中給出
$$
V^*(s) = \max_\pi V^\pi(s)
$$
表示在所有可能的 policy 中，找出能讓 state ( s ) 的價值最大的那個。也就是說，最佳 value function 代表「若採用最佳策略，從該 state 出發最多能期待拿到多少回報」。

---

#### 8. 下列何者最能描述 Bellman equation 的核心精神？ （來源題號：8）

- A. 將問題一次算完，不可拆分
- B. 利用遞迴把目前價值寫成即時 reward 與未來價值的組合
- C. 只考慮 immediate reward
- D. 完全不考慮 state transition

**答案：B**

**詳解：**
Bellman equation 的重要性在於它揭示了 value function 與 Q function 的遞迴結構：目前 state 的價值，可以分解成當前 reward 加上未來 state 價值的折扣期望。這種「大問題拆成子問題」的特性，就是 dynamic programming 能成立的基礎。

---

#### 9. Policy iteration 包含哪兩個主要步驟？ （來源題號：9）

- A. Exploration 與 exploitation
- B. Policy evaluation 與 policy improvement
- C. Sampling 與 replay
- D. Prediction 與 classification

**答案：B**

**詳解：**
PDF 的 Policy Iteration 演算法明確分成兩階段：

1. **Policy Evaluation**：在固定 policy 下計算 ( V(s) )
2. **Policy Improvement**：根據目前的 ( V(s) ) 改善 policy
反覆進行直到 policy stable 為止。

---

#### 10. Value iteration 的更新核心是什麼？ （來源題號：10）

- A. 對所有 action 取平均
- B. 對所有 state 取最小值
- C. 對所有 action 取最大值
- D. 對所有 reward 做排序

**答案：C**

**詳解：**
PDF 中 Value Iteration 的更新式為
$$
V(s) \leftarrow \max_a \sum_{s',r} p(s',r|s,a)[r+\gamma V(s')]
$$
可見它對 action 做 maximization，因此每次都直接往更好的 action 靠近，而不是先完整評估 policy 再改善。這也是它相對簡潔的原因。

---

#### 11. Monte Carlo 方法在 PDF 中被描述為哪一類方法？ （來源題號：11）

- A. Model-based
- B. Model-free
- C. Supervised
- D. Deterministic

**答案：B**

**詳解：**
PDF 直接寫出：Monte Carlo (MC) is a **Model Free method**。也就是說，MC 不需要知道完整的環境轉移機率或 reward model，而是透過實際 sample 到的 episode return 來估計 value 或 Q。

---

#### 12. Sarsa 屬於哪一種控制方法？ （來源題號：12）

- A. On-policy TD control
- B. Off-policy TD control
- C. Model-based planning
- D. Dynamic programming

**答案：A**

**詳解：**
PDF 中直接說明：Sarsa is an **on-policy TD control**。
它的更新會使用實際按照當前 policy 選出的下一個 action $a_{t+1}$，因此學習的目標與行為策略一致，屬於 on-policy。

---

#### 13. Q-learning 屬於哪一種類型？ （來源題號：13）

- A. On-policy
- B. Off-policy
- C. Monte Carlo only
- D. Policy iteration only

**答案：B**

**詳解：**
PDF 雖然在標題寫的是 Temporal Difference - Q Learning，但從更新式可看出它使用
$$
r + \gamma \max_{a'} Q(s',a')
$$
這裡的下一步採用的是「最佳可能 action」的值，而不是實際依當前行為 policy 選出的 action，因此 Q-learning 屬於 off-policy 方法。

---

#### 14. Deep Q Learning 以什麼取代傳統的 Q function 表示方式？ （來源題號：14）

- A. 決策樹
- B. 線性回歸
- C. 深度神經網路
- D. K-means

**答案：C**

**詳解：**
PDF 指出，Deep Q Learning 以一個 deep neural network，也就是 Q-network，來近似 Q function。這讓方法能處理較大的 state space，而不必像 tabular Q-learning 那樣為每個 state-action pair 都存一個明確表格值。

---

#### 15. Deep Q Learning 中的 replay memory 主要用來儲存什麼？ （來源題號：15）

- A. 只有 states
- B. 只有 rewards
- C. transitions
- D. 只有 actions

**答案：C**

**詳解：**
PDF 的 DQL 演算法中寫到要將 transition
$$
(s, a, r, s')
$$
存入 replay memory ( D )。之後再從 ( D ) 中隨機抽 minibatch 訓練。換句話說，memory 裡不是只存 state 或 reward，而是完整的 transition 經驗。

---

### 中等

#### 16. 下列對 return $G_t$ 的敘述何者正確？ （來源題號：16）

- A. 只包含當前 reward
- B. 只包含未來第一步 reward
- C. 是未來 reward 的折扣總和
- D. 與 discount factor 無關

**答案：C**

**詳解：**
根據 PDF，
$$
G_t = \sum_{k=0}^{H}\gamma^k r_{t+k+1}
$$
return 是未來多個 reward 經過折扣後的加總，因此不是只有當下 reward，也不會與$\gamma$ 無關。

---

#### 17. 當 $\gamma$ 越接近 1 時，代表 Agent 傾向如何？ （來源題號：17）

- A. 只重視短期 reward
- B. 完全忽略未來
- C. 更重視長期 reward
- D. 不再需要 policy

**答案：C**

**詳解：**
當 $\gamma$ 越大，未來 reward 被折扣得越少，因此長期回報對目前決策的影響越大。反之，若 $\gamma$ 很小，Agent 會偏向短視近利，只重視近期 reward。

---

#### 18. Bellman equation 中，( V^\pi(s) ) 會對哪個變數做加權平均？ （來源題號：18）

- A. 只對 state
- B. 只對 reward
- C. 先對 action，再對可能的轉移結果
- D. 只對 policy

**答案：C**

**詳解：**
PDF 中的 Bellman equation 顯示
$$
V^\pi(s)=\sum_a \pi(a|s)\sum_{s',r}p(s',r|s,a)\left[r+\gamma V^\pi(s')\right]
$$
先依照 policy$\pi(a|s)$ 對 action 加權，再依照 transition probability 對 ( s',r ) 加權。因此答案是先對 action，再對可能結果加權。

---

#### 19. 下列哪一項最符合 Bellman optimality 的想法？ （來源題號：19）

- A. 對 action 取平均
- B. 對 action 取最大值
- C. 固定 policy 不變
- D. 只更新 reward

**答案：B**

**詳解：**
在最佳化情境下，我們希望每個 state 都選擇最好的 action，因此 value iteration 和 optimal value 的表示都會出現 max over actions。這正是 Bellman optimality 的精神：用最佳可能選擇來定義 state 的最優價值。

---

#### 20. 根據 PDF，( V^*(s) ) 與 ( q^*(s,a) ) 的關係為何？ （來源題號：20）

- A. ( V^*(s)=\min_a q^*(s,a) )
- B. ( V^*(s)=\max_a q^*(s,a) )
- C. ( V^*(s)=\sum_a q^*(s,a) )
- D. ( V^*(s)=q^*(s,s) )

**答案：B**

**詳解：**
PDF 明確寫出
$$
V^*(s)=\max_{a\in A(s)} q^{\pi^*}(s,a)
$$
意思是：某一狀態在最佳 policy 下的價值，等於在那個狀態中所有可選 action 裡，最佳 action 所對應的 Q 值。

---

#### 21. Policy iteration 何時可以停止？ （來源題號：21）

- A. 當所有 reward 都變成 0
- B. 當 $\gamma = 0$
- C. 當 policy stable
- D. 當 action 數量固定

**答案：C**

**詳解：**
PDF 在 policy improvement 後檢查 `policy-stable`。若舊 action 與更新後 action 不再改變，表示 policy 已穩定，可以回傳近似最佳的 $V^*$與$\pi^*$。因此停止條件是 policy stable。

---

#### 22. Value iteration 與 policy iteration 的主要差異之一是？ （來源題號：22）

- A. Value iteration 不使用 Bellman equation
- B. Value iteration 將 evaluation 與 improvement 合併
- C. Policy iteration 不需要 state
- D. Value iteration 只適用於 model-free

**答案：B**

**詳解：**
PDF 提到 value iteration 可以避免等到 ( V(s) ) 完全收斂才 improvement，而是把 truncated policy evaluation 和 policy improvement 合併成一次更新。這就是它與 policy iteration 的關鍵差異。

---

#### 23. Monte Carlo first-visit 的更新依據是？ （來源題號：23）

- A. 每次出現 state-action 都更新
- B. 第一個出現的 state-action 之後的 return
- C. 最大 Q 值
- D. TD error

**答案：B**

**詳解：**
PDF 的 Monte Carlo first-visit 演算法說明：對 episode 中出現的每一個 state-action pair，取該 pair **第一次出現**之後的 return ( G )，加入 Returns(s,a)，再更新 ( Q(s,a) ) 為平均值。這是 first-visit 的核心。

---

#### 24. 在非平穩問題中，Monte Carlo 對 $V(S_t)$ 的更新式使用了哪個參數來控制遺忘舊經驗的程度？ （來源題號：24）

- A. $\gamma$
- B. $\theta$
- C. $\alpha$
- D. $\lambda$

**答案：C**

**詳解：**
PDF 給出非平穩問題中的 MC 更新：
$$
V(S_t) \leftarrow V(S_t) + \alpha [G_t - V(S_t)]
$$
其中 $\alpha$ 是 learning rate，也被說明為 "how much we want to forget about past experiences"。因此答案是 $\alpha$。

---

#### 25. Sarsa 的更新式使用哪一個目標？ （來源題號：25）

- A. ( r + \gamma \max_{a'}Q(s',a') )
- B. ( r + \gamma Q(s',a') )，其中 ( a' ) 為實際依 policy 選出的 action
- C. 只用 ( r )
- D. 只用 ( Q(s,a) )

**答案：B**

**詳解：**
Sarsa 的更新式為
$$
Q(s_t,a_t) \leftarrow Q(s_t,a_t) + \alpha [r_t + \gamma Q(s_{t+1}, a_{t+1}) - Q(s_t,a_t)]
$$
這裡的 $a_{t+1}$ 是根據當前 policy 選出的下一動作，而不是取最大值，因此它是 on-policy。

---

#### 26. Q-learning 的更新目標與 Sarsa 最大不同在於什麼？ （來源題號：26）

- A. Q-learning 不使用 reward
- B. Q-learning 使用下一步實際執行的 action
- C. Q-learning 使用下一 state 的最大 Q 值
- D. Q-learning 不使用 learning rate

**答案：C**

**詳解：**
Q-learning 的更新式為
$$
Q(s,a)\leftarrow Q(s,a)+\alpha\left[r+\gamma \max_{a'}Q(s',a')-Q(s,a)\right]
$$
它不是跟著實際 policy 選到的下一個 action，而是直接看下一 state 中最好的 action 值，因此與 Sarsa 的最大差異就是使用 ( \max_{a'}Q(s',a') )。

---

#### 27. n-step Sarsa 中，n-step Q-return 的特點是？ （來源題號：27）

- A. 完全不看未來
- B. 只使用 1-step reward
- C. 累積前 n 步 reward，再接 bootstrap 項
- D. 只看 terminal reward

**答案：C**

**詳解：**
PDF 給出 n-step return：前面累積數步 reward，最後再加上一個 $\gamma^n Q(S_{t+n})$ 的 bootstrap 項。也就是說，它介於純 MC 和 1-step TD 之間，是多步回報與 bootstrapping 的結合。

---

#### 28. Forward-view Sarsa($\lambda$) 的 $q_t^\lambda$ 是什麼？ （來源題號：28）

- A. 單一步 return
- B. 對不同 n-step return 做加權和
- C. 最佳 policy
- D. 單純的 reward 平均值

**答案：B**

**詳解：**
PDF 顯示
$$
q_t^\lambda = (1-\lambda) \sum_{n=1}^{\infty} \lambda^{n-1} q_t^{(n)}
$$
表示它把不同長度的 n-step return 依照 $\lambda$ 做加權整合，所以不是單一 return，而是多個 n-step return 的混合。

---

#### 29. Temporal Difference 方法的核心特性是什麼？ （來源題號：29）

- A. 必須完整知道環境模型
- B. 用估計值取代完整 episode return
- C. 一定等整個 episode 結束才更新
- D. 只適用於 deterministic 環境

**答案：B**

**詳解：**
PDF 指出 TD methods 直接從 raw experience 學習，不需要環境 model，且它用
$$
R_{t+1} + \gamma V(S_{t+1})
$$
這種估計值來取代完整的 $G_t$。這就是 bootstrapping，也代表它不一定要等 episode 結束才更新。

---

#### 30. TD 對 value 的更新式中，目標值是什麼？ （來源題號：30）

- A. ( V$S_t$ )
- B. ( R_{t+1} + \gamma V$S_{t+1}$ )
- C. ( \max_a Q$S_t,a$ )
- D. $G_t$ 的完整總和

**答案：B**

**詳解：**
PDF 給出的 TD 更新為
$$
V(S_t) \leftarrow V(S_t) + \alpha \bigl[R_{t+1} + \gamma V(S_{t+1}) - V(S_t)\bigr]
$$
所以它使用的目標是「當前 reward + 下一 state value 的折扣估計」，而不是完整 episode return。

---

#### 31. 在 PDF 的 Q-learning 演算法中，選 action 時常使用哪種策略？ （來源題號：31）

- A. Beam search
- B. $\epsilon$-greedy
- C. BFS
- D. Backtracking

**答案：B**

**詳解：**
PDF 在 Q-learning 演算法中提到：Choose $a$ from $s$ using policy derived from Q (e.g., $\epsilon$-greedy)。這表示常見的做法是用 $\epsilon$-greedy 來平衡 exploration 與 exploitation。

---

#### 32. $\epsilon$-greedy 中，$\epsilon$ 的作用是什麼？ （來源題號：32）

- A. 控制 discount
- B. 控制隨機探索的機率
- C. 控制 learning rate
- D. 控制 replay memory 大小

**答案：B**

**詳解：**
在 $\epsilon$-greedy 中，大部分時間選目前估計最好的 action，但有機率 $\epsilon$ 隨機探索其他 action。這樣可避免過早陷入局部最佳。

---

#### 33. Deep Q Learning 的 loss $L_i(\theta_i)$ 中，prediction 是什麼？ （來源題號：33）

- A. ( r+\gamma \max_{a'}Q(s',a';\theta_{i-1}) )
- B. $Q(s,a;\theta_i)$
- C. ( V(s) )
- D. $\pi(a|s)$

**答案：B**

**詳解：**
PDF 在 DQL 的 loss 公式中標示得很清楚：

- target：( r+\gamma \max_a Q(s',a';\theta_{i-1}) )
- prediction：$Q(s,a;\theta_i)$
因此 prediction 就是目前網路對該 state-action pair 所做的 Q 值預測。

---

#### 34. 在 DQL 中，target value 主要由哪兩部分組成？ （來源題號：34）

- A. reward 與 policy probability
- B. reward 與 discounted future max Q
- C. state 與 action
- D. replay memory 與 learning rate

**答案：B**

**詳解：**
從 PDF 的 target 可看出，非 terminal 狀態時
$$
y_j = r_j + \gamma \max_a Q(s'_j,a';\theta)
$$
因此它由即時 reward 和未來最佳 Q 值的折扣部分組成。若是 terminal state，則只有 $r_j$。

---

#### 35. 在 DQL 中，若 $s'_j$ 是 terminal state，則 $y_j$ 應設為何？ （來源題號：35）

- A. ( 0 )
- B. ( \gamma \max_a Q$s'_j,a'$ )
- C. $r_j$
- D. ( r_j + Q$s_j,a_j$ )

**答案：C**

**詳解：**
PDF 在演算法裡明確寫到：
- terminal $s'_j$：$y_j = r_j$
- non-terminal $s'_j$：$y_j = r_j + \gamma \max_a Q(s'_j,a')$
因為終止狀態之後沒有未來回報，所以 target 只剩下當前 reward。

---

### 困難

#### 36. 為什麼 Bellman equation 對 RL 很重要？ （來源題號：36）

- A. 因為它讓 reward 變成常數
- B. 因為它揭示 value function 的遞迴結構
- C. 因為它取消了 transition probability
- D. 因為它等價於神經網路

**答案：B**

**詳解：**
Bellman equation 讓我們把「當前 state 的價值」寫成「即時 reward + 未來 state 的價值」，形成遞迴結構。這種特性讓 policy evaluation、value iteration 等方法都能成立，也是 dynamic programming 的核心基礎。PDF 特別強調 expanding value/Q 後會出現這種重要 recursive property。

---

#### 37. Q-learning 為什麼通常被視為 off-policy？ （來源題號：37）

- A. 因為它不更新 Q 值
- B. 因為它更新時不依賴任何 action
- C. 因為它更新目標使用 greedy 的最大 Q，而非實際行為 policy 的下一動作
- D. 因為它一定使用 Monte Carlo

**答案：C**

**詳解：**
Q-learning 的更新是看下一 state 中的最大 Q 值，即假設未來會採用最優 action；但實際行動時可能還是透過 $\epsilon$-greedy 等策略探索。也就是說，行為 policy 與學習目標 policy 可以不同，因此它是 off-policy。

---

#### 38. Sarsa 與 Q-learning 的根本差異最準確的描述是？ （來源題號：38）

- A. 一個用 state，另一個不用 state
- B. 一個用 learning rate，另一個不用
- C. 一個根據實際選到的下一 action 更新，另一個根據下一 state 的最佳 action 更新
- D. 一個只適合神經網路，另一個只適合表格法

**答案：C**

**詳解：**
Sarsa 的更新依據是 ( Q(s',a') )，其中 ( a' ) 是根據目前 policy 實際選出的下一動作；Q-learning 則用 ( \max_{a'}Q(s',a') )，直接朝理論上最佳動作學習。這就是 on-policy 與 off-policy 的典型差異。

---

#### 39. Monte Carlo first-visit 與 every-visit 的概念差異中，根據 PDF 可以確定的是？ （來源題號：39）

- A. PDF 採用 every-visit
- B. PDF 明確使用 first-visit
- C. PDF 不更新 Q 值
- D. PDF 只更新 policy，不更新 value

**答案：B**

**詳解：**
PDF 的演算法標題就叫 **Monte Carlo first-visit**，並在步驟中說明「return following the first occurrence of s, a」。因此可確定它採用的是 first-visit，而不是 every-visit。

---

#### 40. 為何 value iteration 通常比完整的 policy iteration 更直接？ （來源題號：40）

- A. 因為它不需要 reward
- B. 因為它省略了 policy evaluation
- C. 因為它把 improvement 和 truncated evaluation 合成一次更新
- D. 因為它只在 terminal state 更新

**答案：C**

**詳解：**
PDF 明確指出 value iteration 避免等到 ( V(s) ) 完全收斂，而是把 policy improvement 與 truncated policy evaluation 合併成一個操作。因此它的更新路徑更直接。這不是完全不做 evaluation，而是把 evaluation 簡化並和 improvement 結合。

---

#### 41. TD 方法相對 MC 的一個重要特徵是 bootstrapping。這代表什麼？ （來源題號：41）

- A. 用真實完整 return 更新
- B. 用目前估計的 value 作為更新目標的一部分
- C. 不使用 reward
- D. 不使用 state transition

**答案：B**

**詳解：**
TD 的更新式中含有 $V(S_{t+1})$ 或 $Q(s',a')$ 這類「目前估計值」，表示它用自己的估計輔助更新自己，這就是 bootstrapping。與 MC 使用完整 sample return 相比，TD 更早更新，但也引入估計誤差來源。

---

#### 42. Monte Carlo 方法通常變異較大的主要原因是什麼？ （來源題號：42）

- A. 它完全不用 reward
- B. 它一定需要環境模型
- C. 它依賴整條 episode 的實際 return
- D. 它只能用於 deterministic 環境

**答案：C**

**詳解：**
MC 直接用 sample return $G_t$ 更新，這個 return 可能受到整條 episode 中後續隨機性的影響，因此估計波動通常較大。雖然 PDF 沒直接寫 variance 一詞，但從其「averaging sample returns」與完整 return 機制可合理推得這點。這是依 PDF 內容作出的推論。

---

#### 43. n-step Sarsa 可被視為在何者之間折衷？ （來源題號：43）

- A. DP 與 supervised learning
- B. 1-step TD 與 Monte Carlo
- C. Policy iteration 與 value iteration
- D. Q-network 與 replay memory

**答案：B**

**詳解：**
n-step Sarsa 前面累積多步實際 reward，但最後仍接一個 bootstrap 的 $Q(S_{t+n})$ 項。因此它不像 1-step TD 那麼短視，也不像 MC 那樣要等完整 episode，正好處於兩者之間。

---

#### 44. 在 Forward-view Sarsa($\lambda$) 中，$\lambda$ 的功能最接近下列何者？ （來源題號：44）

- A. 控制不同 n-step return 的權重分配
- B. 控制 discount factor
- C. 控制 replay memory 大小
- D. 控制 terminal state 數量

**答案：A**

**詳解：**
PDF 給出 $$q_t^\lambda = (1-\lambda)\sum_{n=1}^{\infty}\lambda^{n-1}q_t^{(n)}$$，由這個式子可看出，$\lambda$ 是用來調整不同 n-step returns 權重的參數。它不是 discount factor，discount factor 是 $\gamma$。

---

#### 45. Deep Q Learning 中使用 replay memory 的一個重要目的為何？ （來源題號：45）

- A. 讓 action 數量增加
- B. 儲存 policy 公式
- C. 從經驗中隨機抽樣以訓練網路
- D. 讓 reward 固定

**答案：C**

**詳解：**
PDF 描述 DQL 會把 transition 存進記憶體 ( D )，之後 sample random minibatch of transitions 來訓練。這代表 replay memory 的核心用途之一就是讓網路從已收集的經驗中隨機抽樣學習，而不是照原始時間順序直接學。

---

#### 46. DQL loss 公式中的 target 與 prediction 使用不同參數或時間點的估計，其主要用意是？ （來源題號：46）

- A. 讓 Q 值永遠為 0
- B. 使訓練目標更穩定
- C. 取消 discount factor
- D. 取代 replay memory

**答案：B**

**詳解：**
PDF 的 loss 式寫成 prediction 與 target 的平方差，target 使用的是前一輪或另一時間點的估計 $\theta_{i-1}$，prediction 用目前參數 $\theta_i$。這種分離可以避免目標與預測同時劇烈變動，讓訓練較穩。這是從公式結構可直接理解出的功能。

---

#### 47. 在 policy iteration 的 improvement 步驟中，更新 policy 的依據是什麼？ （來源題號：47）

- A. 任意挑一個 action
- B. 選擇使 ( \sum_{s',r}p(s',r|s,a)[r+\gamma V(s')] ) 最大的 action
- C. 選 reward 最小的 action
- D. 選最少出現的 action

**答案：B**

**詳解：**
PDF 的 policy improvement 寫成
$$
\pi(s)\leftarrow \arg\max_a \sum_{s',r}p(s',r|s,a)[r+\gamma V(s')]
$$
意思是根據目前的 value function，挑出能使期望回報最大的 action。這正是 greedy improvement。

---

#### 48. 在 value iteration 收斂後，輸出的 deterministic policy 如何取得？ （來源題號：48）

- A. 對每個 state 隨機選 action
- B. 固定沿用初始 policy
- C. 對每個 state 選擇使 Bellman 更新式最大的 action
- D. 直接取 reward 最大的 state

**答案：C**

**詳解：**
PDF 最後寫出輸出 policy 為
$$
\pi(s)=\arg\max_a \sum_{s',r}p(s',r|s,a)[r+\gamma V(s')]
$$
也就是對每個 state，選出在 value iteration 收斂後最能提高 value 的那個 action。這樣得到的是 deterministic policy。

---

#### 49. 根據 PDF，Deep Q Learning 中若採用 $\epsilon$-greedy，則選 action 的方式為何？ （來源題號：49）

- A. 永遠隨機
- B. 永遠選最小 Q 值
- C. 以機率 $\epsilon$ 隨機選 action，否則選目前 Q 最大的 action
- D. 先選 reward 最大的 state 再選 action

**答案：C**

**詳解：**
PDF 在 DQL 演算法中寫道：以機率 $\epsilon$ 隨機選 action，否則選擇 $a = \max_a Q(s,a;\theta)$。這就是 $\epsilon$-greedy 的標準定義。

---

#### 50. 下列哪一項最能總結這份 PDF 對 RL 方法的鋪陳順序？ （來源題號：50）

- A. 先講 Deep Learning，再講 MDP
- B. 從基本 RL 概念與 MDP 開始，接著 value/Q、Bellman、DP、MC、TD，到 DQL
- C. 只介紹 Sarsa 與 Q-learning
- D. 只介紹神經網路方法

**答案：B**

**詳解：**
這份 cheat sheet 的內容順序很清楚：先從 Agent-Environment Interface、Policy、Reward、MDP、Value Function、Q Function、Bellman Equation 開始，再介紹 Dynamic Programming（Policy Iteration、Value Iteration）、Monte Carlo、Sarsa、Q-learning，最後進到 Deep Q Learning。它是一份從基礎到進階的總覽式整理。

---

## Gemini

### 簡單

#### 51. 在強化學習的代理人與環境介面中，代理人在每一時間步 $t$ 會接收到環境的何種資訊？ （來源題號：1）

- A. 獎勵 $R_t$
- B. 動作 $A_t$
- C. 狀態表徵 $S_t$
- D. 轉移機率 $P$

**答案：C**

**詳解：**
代理人在每一步 $t$ 接收環境狀態的表徵 $S_t \in S$。

---

#### 52. 代理人執行動作 $A_t$ 後，從環境獲得的數值回饋稱為？ （來源題號：2）

- A. 狀態 (State)
- B. 獎勵 (Reward)
- C. 策略 (Policy)
- D. 價值 (Value)

**答案：B**

**詳解：**
作為動作的結果，代理人會收到一個獎勵 $R_{t+1}$。

---

#### 53. 策略 (Policy) $\pi$ 的定義為何？ （來源題號：3）

- A. 從動作到獎勵的對映
- B. 從狀態到動作的對映
- C. 環境的物理規律
- D. 累積獎勵的總和

**答案：B**

**詳解：**
策略是從狀態到動作的對映 $\pi_t(s|a)$。

---

#### 54. 在總獎勵公式中，$\gamma$ 代表什麼參數？ （來源題號：4）

- A. 學習率
- B. 步長
- C. 折扣因子 (Discount factor)
- D. 隨機探索率

**答案：C**

**詳解：**
在 $G_t$ 的計算中，$\gamma$ 是折扣因子。

---

#### 55. 馬可夫決策過程 (MDP) 是由幾個元素組成的多元組 (Tuple)？ （來源題號：5）

- A. 3
- B. 4
- C. 5
- D. 6

**答案：C**

**詳解：**
MDP 是一個 5-tuple $$
S, A, P, R, \gamma
$$
。

---

#### 56. 狀態價值函數 $V_\pi(s)$ 衡量的是什麼？ （來源題號：6）

- A. 在狀態 $s$ 下執行特定動作的好壞
- B. 環境發生變化的機率
- C. 在特定策略下處於狀態 $s$ 的預期長期回報
- D. 代理人移動的速度

**答案：C**

**詳解：**
價值函數描述在特定策略下處於特定狀態 $s$ 有多好。

---

#### 57. 蒙地卡羅 (Monte Carlo) 方法的主要特點是什麼？ （來源題號：7）

- A. 需要完整的環境模型
- B. 是一種 Model-Free (無模型) 方法
- C. 僅能處理連續狀態
- D. 不需要任何取樣

**答案：B**

**詳解：**
蒙地卡羅法是 Model Free 方法，不需要環境動態的完整知識。

---

#### 58. Sarsa 演算法名稱中的 "r" 代表什麼？ （來源題號：8）

- A. 狀態 (State)
- B. 動作 (Action)
- C. 獎勵 (Reward)
- D. 學習率 (Rate)

**答案：C**

**詳解：**
Sarsa 代表 State-action-reward-state-action。

---

#### 59. 在非平穩問題中，更新公式裡的 $\alpha$ 代表？ （來源題號：9）

- A. 折扣因子
- B. 學習率 (Learning rate)
- C. 遺忘因子
- D. 衰減率

**答案：B**

**詳解：**
$\alpha$ 是學習率，決定忘記過去經驗的程度。

---

#### 60. Q-Learning 屬於哪種學習方法？ （來源題號：10）

- A. 時序差分 (Temporal Difference)
- B. 動態規劃 (Dynamic Programming)
- C. 暴力搜索法
- D. 監督式學習

**答案：A**

**詳解：**
Q-Learning 是時序差分 (TD) 方法的一種。

---

#### 61. 深度 Q 學習 (DQL) 是由哪個機構提出的？ （來源題號：11）

- A. OpenAI
- B. Facebook AI Research
- C. DeepMind
- D. Google Brain

**答案：C**

**詳解：**
DQL 是由 DeepMind 創造的。

---

#### 62. 在 DQL 中，用來儲存過去經驗以便訓練的機制稱為？ （來源題號：12）

- A. 策略梯度
- B. 經驗回放 (Experience Replay)
- C. 貝氏推論
- D. 神經網絡優化

**答案：B**

**詳解：**
DQL 將觀察結果儲存在記憶中（replay memory）以訓練網絡。

---

#### 63. MDP 中的 $S$ 代表什麼集合？ （來源題號：13）

- A. 獎勵集合
- B. 動作集合
- C. 有限狀態集合
- D. 策略集合

**答案：C**

**詳解：**
$S$ 代表有限的狀態集合，且 $s \in S$。

---

#### 64. $G_t = \sum_{k=0}^{H}\gamma^{k}r_{t+k+1}$ 中，$H$ 代表？ （來源題號：14）

- A. 熵 (Entropy)
- B. 地平線/步數限制 (Horizon)
- C. 隱藏層數量
- D. 歷史長度

**答案：B**

**詳解：**
$H$ 是地平線 (horizon)，可以是無限的。

---

#### 65. 最優價值函數 (Optimal Value Function) 的符號標記為？ （來源題號：15）

- A. $V_\pi(s)$
- B. $V_*(s)$
- C. $q_\pi(s, a)$
- D. $G_t$

**答案：B**

**詳解：**
最優價值函數標記為 $V_*(s)$。

---

### 中等

#### 66. 狀態轉移機率 $p(s'|s,a)$ 代表的意義是？ （來源題號：16）

- A. 在狀態 $s(採取動作)a$ 得到獎勵的機率
- B. 在狀態 $s(採取動作)a$後轉移到狀態$s'$ 的機率
- C. 執行策略 $\pi$ 的機率
- D. 從 $s'$回到$s$ 的機率

**答案：B**

**詳解：**
這是轉移機率的定義：$Pr\{S_{t+1}=s' \mid S_t=s, A_t=a\}$。

---

#### 67. 動作價值函數 $q_\pi(s,a)$ 與狀態價值函數 $V_\pi(s)$ 的主要區別在於？ （來源題號：17）

- A. $q$ 函數不考慮獎勵
- B. $V$ 函數考慮了特定的動作對 (state-action pair)
- C. $q(函數衡量在狀態)s$採取特定動作$a$ 後的預期回報
- D. $V$ 函數只適用於離散空間

**答案：C**

**詳解：**
$q_\pi(s,a)$ 標註了狀態與動作對的預期回報。

---

#### 68. 貝爾曼方程 (Bellman Equation) 的核心特性是什麼？ （來源題號：18）

- A. 線性特性
- B. 遞迴特性 (Recursive property)
- C. 發散特性
- D. 卷積特性

**答案：B**

**詳解：**
展開價值函數與 Q 函數時會出現重要的遞迴特性。

---

#### 69. 策略迭代 (Policy Iteration) 演算法包含哪兩個主要步驟？ （來源題號：19）

- A. 初始化與終止
- B. 策略評估與策略改進
- C. 隨機取樣與期望計算
- D. 卷積與池化

**答案：B**

**詳解：**
策略迭代包含 Policy Evaluation 與 Policy Improvement。

---

#### 70. 策略評估 (Policy Evaluation) 通常在何時停止？ （來源題號：20）

- A. 執行固定 100 次後
- B. 當價值函數的變化量 $\Delta(小於閾值)\theta$ 時
- C. 當獲得正獎勵時
- D. 當代理人到達終點時

**答案：B**

**詳解：**
當 $\Delta < \theta$ 時停止迴圈。

---

#### 71. 價值迭代 (Value Iteration) 與策略迭代的主要區別是？ （來源題號：21）

- A. 價值迭代不需要 $\gamma$
- B. 價值迭代在單一操作中結合了策略改進與截斷的策略評估
- C. 策略迭代速度總是比價值迭代快
- D. 價值迭代只能用於 Model-Free 環境

**答案：B**

**詳解：**
價值迭代避免等待 $V(s)$ 收斂，而是在一步中完成改進與評估。

---

#### 72. 蒙地卡羅首次訪問 (First-visit MC) 方法如何估算 $Q(s,a)$？ （來源題號：22）

- A. 計算單次最高獎勵
- B. 平均每個狀態動作對的樣本回報 (Sample returns)
- C. 使用神經網絡預測
- D. 計算狀態轉移的機率和

**答案：B**

**詳解：**
它是基於對每個狀態動作對的樣本回報取平均值。

---

#### 73. Sarsa 更新規則 $Q(s_t,a_t) \leftarrow Q(s_t,a_t) + \alpha[r_t + \gamma Q(s_{t+1},a_{t+1}) - Q(s_t,a_t)]$ 表現了什麼？ （來源題號：23）

- A. 它是 Off-policy 更新
- B. 它使用下一個狀態與「實際採取的下一個動作」來更新
- C. 它不需要學習率 $\alpha$
- D. 它不考慮折扣因子

**答案：B**

**詳解：**
Sarsa 使用 $Q(s_{t+1}, a_{t+1})$，也就是當前策略實際選出的下一個動作對應的值來更新。

---

#### 74. 時序差分 (TD) 方法相對於蒙地卡羅法的優勢是？ （來源題號：24）

- A. TD 需要完整的片段才能更新
- B. TD 可以直接從原始經驗中學習，不需要環境模型
- C. TD 的方差總是比 MC 高
- D. TD 不需要折扣因子

**答案：B**

**詳解：**
TD 方法直接從經驗中學習且無需環境動態模型。

---

#### 75. Q-Learning 的更新式中，為什麼被稱為 Off-policy？ （來源題號：25）

- A. 因為它不使用 $\gamma$
- B. 因為它在更新時使用了 $max_{a'}$ 操作，而非實際執行的動作
- C. 因為它不紀錄狀態
- D. 因為它只在片段結束時更新

**答案：B**

**詳解：**
更新式中使用 $max_{a'}Q(s',a')$，這與代理人實際遵循的策略可能不同。

---

#### 76. 在 DQL 的損失函數 (Loss Function) 中，目標 (Target) 項包含什麼？ （來源題號：26）

- A. 只有當前獎勵 $r$
- B. $r + \gamma max_{a'} Q(s', a'; \theta_{i-1})$
- C. $Q(s, a; \theta_i)$
- D. $\pi(a|s)$

**答案：B**

**詳解：**
根據損失函數公式，目標項為 $r + \gamma max_{a'} Q(s', a'; \theta_{i-1})$。

---

#### 77. 蒙地卡羅方法中的 $G$ 代表？ （來源題號：27）

- A. 隨機變數
- B. 片段中某次出現後的樣本回報 (Return)
- C. 梯度 (Gradient)
- D. 貪婪度 (Greediness)

**答案：B**

**詳解：**
$G$ 是在片段中狀態動作對出現後的樣本回報。

---

#### 78. 動態規劃 (Dynamic Programming) 在 RL 中主要利用了什麼結構？ （來源題號：28）

- A. 隨機結構
- B. 子問題結構 (Subproblem structure)
- C. 循環結構
- D. 線性結構

**答案：B**

**詳解：**
DP 利用 $V(與)Q$ 函數的子問題結構進行規劃。

---

#### 79. 如果 $H$（Horizon）是無限的，為了保證總回報 $G_t$ 收斂，$\gamma$ 必須滿足？ （來源題號：29）

- A. $\gamma > 1$
- B. $\gamma = 1$
- C. $0 \le \gamma < 1$
- D. $\gamma = -1$

**答案：C**

**詳解：**
在無限地平線下，折扣因子須小於 1 以確保級數收斂。

---

#### 80. $n$-step Sarsa 更新目標與 1-step Sarsa 的主要不同在於？ （來源題號：30）

- A. 使用了神經網絡
- B. 累積了 $n(步的獎勵加上第)n$ 步的估計值
- C. 不需要獎勵 $R$
- D. 它是 Off-policy

**答案：B**

**詳解：**
$n$-step Q-Return 包含 $n$ 步獎勵的折扣和，以及最後的 bootstrap 項 $Q(S_{t+n})$。

---

#### 81. 策略迭代中，若 `old-action == pi(s)` 對所有狀態都成立，表示？ （來源題號：31）

- A. 演算法出錯
- B. 策略已穩定 (Policy-stable) 並收斂至最優
- C. 需增加學習率
- D. 環境已改變

**答案：B**

**詳解：**
當動作不再改變，說明策略已穩定並逼近最優策略 $\pi_*$。

---

#### 82. 在 MDP 中，期望獎勵 $r(s', s, a)$ 的定義涉及哪些變數？ （來源題號：32）

- A. 只有當前狀態 $s$
- B. 下一狀態 $s'$、當前狀態 $s(與動作)a$
- C. 只有策略 $\pi$
- D. 只有動作 $a$

**答案：B**

**詳解：**
定義為 $\mathbb{E}[R_{t+1}|S_{t+1}=s', S_t=s, A_t=a]$。

---

#### 83. DQL 使用 `Experience Replay` 的主要目的是？ （來源題號：33）

- A. 增加計算難度
- B. 打破資料間的相關性並重複利用過去經驗訓練
- C. 減少記憶體消耗
- D. 強制代理人忘記過去

**答案：B**

**詳解：**
透過從歷史中取樣 minibatch 訓練，可穩定網絡更新。

---

#### 84. 在時序差分學習中，$V(S_t)$ 的更新朝向哪個目標？ （來源題號：34）

- A. $G_t$
- B. $R_{t+1} + \gamma V(S_{t+1})$
- C. $V(S_{t-1})$
- D. $\arg\max_a Q(s, a)$

**答案：B**

**詳解：**
TD 更新是朝向 TD 目標 $R_{t+1} + \gamma V(S_{t+1})$。

---

#### 85. 下列何者描述了最優策略 $\pi_*$與最優價值函數$V_*$ 的關係？ （來源題號：35）

- A. $V_*$ 總是等於 0
- B. 最優狀態價值等於從該狀態出發的最佳動作的期望回報
- C. $V_*$與$\pi_*$ 無關
- D. $\pi_*$ 總是隨機的

**答案：B**

**詳解：**
方程 8 表達了 $V_*(s) = max_a q_{\pi*}(s, a)$。

---

### 困難

#### 86. 請推導 Bellman 方程中 $V_\pi(s)$ 的全機率展開形式，下列何者正確？ （來源題號：36）

- A. $V_\pi(s) = \sum_{a}\pi(a|s)\sum_{s',r}p(s',r|s,a)[r + \gamma V_\pi(s')]$
- B. $V_\pi(s) = \sum_{a}\pi(a|s)[R + \gamma V_\pi(s')]$
- C. $V_\pi(s) = max_a \sum_{s'} p(s'|s,a)V_\pi(s')$
- D. $V_\pi(s) = \mathbb{E}[R_{t+1}]$

**答案：A**

**詳解：**
這是價值函數的完整貝爾曼方程展開。

---

#### 87. 在策略改進 (Policy Improvement) 步驟中，新的策略 $\pi(s)$ 是如何選取的？ （來源題號：37）

- A. 隨機選取
- B. $argmax_a \sum_{s', r} p(s', r|s, a) [r + \gamma V(s')]$
- C. 選取價值最小的動作
- D. 保持與舊策略一致

**答案：B**

**詳解：**
策略改進透過對 $Q$ 值估計進行貪婪化操作。

---

#### 88. Forward View Sarsa($\lambda$) 的權重項 $(1-\lambda)\lambda^{n-1}$ 作用為何？ （來源題號：38）

- A. 增加單步獎勵權重
- B. 對不同步數的 $n$-step 回報進行加權平均
- C. 作為神經網絡的激發函數
- D. 計算轉移機率

**答案：B**

**詳解：**
這是 $\lambda$-return 的定義，整合了所有 $n$-step 的回報。

---

#### 89. DQL 的 Loss Function $L_i(\theta_i)$ 中，為什麼 $\theta_{i-1}$ 要加下標 $i-1$？ （來源題號：39）

- A. 代表它是當前正在優化的參數
- B. 代表它是固定住的「目標網路」參數，用以穩定訓練
- C. 代表它是第一層卷積核
- D. 代表它是過往所有權重的總和

**答案：B**

**詳解：**
為了計算目標值，通常會使用前一時刻或固定的網路參數 $\theta_{i-1}$。

---

#### 90. 價值迭代的更新規則 $V(s) \leftarrow max_a \sum_{s',r} p(s',r|s,a)[r + \gamma V(s')]$ 實際上隱含了什麼？ （來源題號：40）

- A. 一次策略評估
- B. 一次策略改進
- C. 在每一步評估後立即進行策略改進
- D. 忽略所有獎勵

**答案：C**

**詳解：**
價值迭代在更新價值時直接取 $max$，省略了顯式的策略步驟。

---

#### 91. 在蒙地卡羅方法更新式 $V(S_t) \leftarrow V(S_t) + \alpha [G_t - V(S_t)]$ 中，$[G_t - V(S_t)]$ 被稱為什麼？ （來源題號：41）

- A. 折扣因子
- B. 預測誤差 (Prediction Error) 或估計殘差
- C. 累積獎勵
- D. 轉移機率

**答案：B**

**詳解：**
這是當前觀測回報與原估計值的差距。

---

#### 92. Sarsa$$
\lambda
$$
的演算法實作中，更新$Q(s,a)$ 是在什麼時機？ （來源題號：42）

- A. 每個片段結束時
- B. 每一時間步，觀察到 $r, s'$並選取$a'$ 後
- C. 只有在到達目標時
- D. 隨機觸發

**答案：B**

**詳解：**
TD 方法（如 Sarsa）在每一步都會進行更新。

---

#### 93. 在 DQL 演算法中，選擇動作時使用的 $\epsilon$-greedy 策略具體指？ （來源題號：43）

- A. 以 $\epsilon$ 機率選擇隨機動作，否則選擇最優動作
- B. 總是選擇獎勵最高的動作
- C. 隨機選取 50% 動作
- D. 只在開始訓練時隨機選取

**答案：A**

**詳解：**
以機率 $\epsilon$ 進行隨機探索，否則選擇使 $Q$ 值最大的動作。

---

#### 94. DQL 損失函數中的預測項 (Prediction) 是什麼？ （來源題號：44）

- A. $r$
- B. $Q(s, a; \theta_i)$
- C. $y_j^*$
- D. $\gamma$

**答案：B**

**詳解：**
預測項是當前網路對狀態動作對的評分 $Q(s, a; \theta_i)$。

---

#### 95. 如果一個 MDP 的狀態轉移是確定的，則 $p(s'|s,a)$ 的取值只可能是？ （來源題號：45）

- A. 0 或 1
- B. 任何 0 到 1 之間的實數
- C. 總是 0.5
- D. 無法計算

**答案：A**

**詳解：**
確定性系統中，給定 $(s,a)$只會有一種特定的$s'$，故機率非 0 即 1。

---

#### 96. $V_*(s) = max_{a \in A(s)} q_{\pi*}(s,a)$ 這一等式成立的前提是？ （來源題號：46）

- A. 代理人採取隨機動作
- B. 代理人遵循最優策略
- C. 獎勵全部為正
- D. 環境是 Model-Free 的

**答案：B**

**詳解：**
最優策略下的價值必須等於該狀態下最佳動作的預期回報。

---

#### 97. 在 DQL 中，若 $s'_j$ 是終止狀態（Terminal State），其目標值 $y_j$ 應設為？ （來源題號：47）

- A. 0
- B. $r_j$
- C. $r_j + \gamma max Q$
- D. $-1$

**答案：B**

**詳解：**
根據 DQL 更新邏輯，若為終止狀態，回報僅為當前獎勵 $r_j$。

---

#### 98. 貝爾曼方程展示了 $q_\pi(s,a)$ 可以用 $V_\pi(s')$ 來表示，其關係式為？ （來源題號：48）

- A. $q_\pi(s,a) = \sum_{s',r} p(s',r|s,a)[r + \gamma V_\pi(s')]$
- B. $q_\pi(s,a) = V_\pi(s)$
- C. $q_\pi(s,a) = r + V_\pi(s)$
- D. $q_\pi(s,a) = \pi(a|s)V_\pi(s)$

**答案：A**

**詳解：**
方程 10 描述了 $Q$ 函數與下一狀態價值函數的遞迴關係。

---

#### 99. 蒙地卡羅方法為何不適用於非片段式 (Non-episodic) 的任務？ （來源題號：49）

- A. 因為它需要太多的記憶體
- B. 因為它需要等到片段結束獲得回報 $G_t$ 才能進行更新
- C. 因為它無法處理折扣因子
- D. 因為它需要環境模型

**答案：B**

**詳解：**
MC 必須生成完整片段 (Generate an episode) 才能獲得回報樣本。

---

#### 100. 在 DQL 訓練中，從經驗回放池 $D$ 中取樣的對象是？ （來源題號：50）

- A. 單一狀態 $s$
- B. 單一動作 $a$
- C. 轉換元組 $(s, a, r, s')$ (Transitions)
- D. 整個策略 $\pi$

**答案：C**

**詳解：**
儲存並取樣的是 $(s, a, r, s')$ 轉換對。

---

## Claude

### 簡單

#### 101. 在 Agent-Environment Interface 中，Agent 在時間步 $t$ 採取動作 $A_t$ 後，環境會回傳什麼？ （來源題號：1）

- A. 下一狀態 $S_{t+1}$和策略$\pi$
- B. 下一狀態 $S_{t+1}$和獎勵$R_{t+1}$
- C. 折扣因子 $\gamma(和動作)A_{t+1}$
- D. 價值函數 $V(s)$和獎勵$R_{t+1}$

**答案：B**

**詳解：**
根據 Agent-Environment Interface，Agent 在每個時間步 $t$ 觀察到狀態 $S_t$，並選擇動作 $A_t$，環境隨後回傳下一狀態 $S_{t+1}$ 與獎勵 $R_{t+1}$。

---

#### 102. 策略（Policy）$\pi_t(s|a)$ 代表什麼？ （來源題號：2）

- A. 在狀態 $s(下執行動作)a$ 的預期獎勵
- B. 在動作 $a(已知的情況下，狀態為)s$ 的機率
- C. 在狀態 $S_t = s(時選擇動作)A_t = a$ 的機率
- D. 在時間步 $t$ 採取所有動作的平均獎勵

**答案：C**

**詳解：**
Policy 是從狀態到動作的映射，$\pi_t(s|a)$ 表示在狀態 $S_t=s$ 時，選擇動作 $A_t=a$ 的機率。

---

#### 103. 總獎勵（Return）的公式 $G_t = \sum_{k=0}^{H} \gamma^k r_{t+k+1}$ 中，$\gamma$ 代表什麼？ （來源題號：3）

- A. 學習率（Learning Rate）
- B. 折扣因子（Discount Factor）
- C. 時間步長（Time Step）
- D. 水平線（Horizon）

**答案：B**

**詳解：**
$\gamma$ 為折扣因子（Discount Factor），範圍通常為 $[0,1]$。它控制未來獎勵相對於即時獎勵的重要性。

---

#### 104. MDP（Markov Decision Process）是由哪 5 個元素組成的元組？ （來源題號：4）

- A. $$
S, A, P, R, \alpha
$$
- B. $$
S, A, Q, R, \gamma
$$
- C. $$
S, A, P, R, \gamma
$$
- D. $$
S, \pi, P, V, \gamma
$$

**答案：C**

**詳解：**
MDP 是一個 5-tuple：$$(S, A, P, R, \gamma)$$ 其中 $S$ 為狀態集合，$A$ 為動作集合，$P$ 為狀態轉移機率，$R$ 為獎勵函數，$\gamma$ 為折扣因子。

---

#### 105. 狀態轉移機率（State Transition Probability）的正確表示為何？ （來源題號：5）

- A. $p(s'|s, a) = Pr\{S_{t+1} = s' | S_t = s\}$
- B. $p(s'|s, a) = Pr\{S_{t+1} = s' | S_t = s, A_t = a\}$
- C. $p(s'|s, a) = Pr\{A_t = a | S_t = s, S_{t+1} = s'\}$
- D. $p(s'|s, a) = E[R_{t+1} | S_t = s, A_t = a]$

**答案：B**

**詳解：**
狀態轉移機率表示在狀態 $s$ 執行動作 $a$ 後，轉移到狀態 $s'$ 的機率，也就是 $p(s'|s,a)$。

---

#### 106. 價值函數 $V_\pi(s)$ 的非正式說明是？ （來源題號：6）

- A. 在狀態 $s$ 執行所有可能動作的最大即時獎勵
- B. 從狀態 $s(出發並遵循策略)\pi$ 的預期累積折扣獎勵
- C. 在策略 $\pi$ 下，執行最優動作的機率
- D. 狀態 $s(和動作)a$ 的聯合機率分布

**答案：B**

**詳解：**
$V_\pi(s)=E[G_t|S_t=s]$，代表從狀態 $s$ 出發並遵循策略 $\pi$ 的預期累積折扣獎勵。

---

#### 107. 最優價值函數 $V^*(s)$ 的定義是？ （來源題號：7）

- A. $V^*(s) = \min_\pi V_\pi(s)$
- B. $V^*(s) = E_\pi[G_t | S_t = s]$
- C. $V^*(s) = \max_\pi V_\pi(s)$
- D. $V^*(s) = \max_a q_\pi(s, a)$

**答案：C**

**詳解：**
最優價值函數 $V^*(s)$定義為所有可能策略中，使$V_\pi(s)$最大的那個值，即$V^*(s) = \max_\pi V_\pi(s)$。選項 D 雖然也正確（是另一個等價表示），但最直接的定義是 C。

---

#### 108. Q 函數（Action-Value Function）$q_\pi(s, a)$ 代表什麼？ （來源題號：8）

- A. 在狀態 $s(下選擇動作)a$ 的機率
- B. 在狀態 $s(執行動作)a$，並遵循策略$\pi$ 的預期回報
- C. 在最優策略下，狀態 $s$ 的最大價值
- D. 在狀態 $s(選擇動作)a$ 後的即時獎勵

**答案：B**

**詳解：**
$q_\pi(s,a)=E_\pi[G_t|S_t=s,A_t=a]$，表示在狀態 $s$ 執行動作 $a$，之後遵循策略 $\pi$ 時的預期回報。

---

#### 109. 最優 Q 函數 $q^*(s, a)$與最優價值函數$V^*(s)$ 的關係為何？ （來源題號：9）

- A. $V^*(s) = \sum_{a \in A(s)} q^*(s, a)$
- B. $V^*(s) = \max_{a \in A(s)} q_{\pi^*}(s, a)$
- C. $V^*(s) = \min_{a \in A(s)} q^*(s, a)$
- D. $V^*(s) = E[q^*(s, a)]$

**答案：B**

**詳解：**
根據教材公式 (8)：$V^*(s) = \max_{a \in A(s)} q_{\pi^*}(s, a)$。直觀上，最優策略下某狀態的價值，等於從該狀態出發選擇最好動作的 Q 值。這個關係連結了狀態價值函數與動作-價值函數。

---

#### 110. 在 Policy Iteration 的初始化步驟中，$\Delta$ 被初始化為何值？ （來源題號：10）

- A. $+\infty$
- B. $\theta$（一個小正數）
- C. $0$
- D. $-\infty$

**答案：C**

**詳解：**
Policy Iteration 初始化時會令 $\Delta \leftarrow 0$，用來追蹤 value function 的最大更新量。

---

#### 111. Policy Evaluation 的迴圈終止條件是什麼？ （來源題號：11）

- A. $\Delta < \theta(（)\theta$ 為一個小正數）
- B. $\Delta \geq \theta$
- C. $\Delta = 0$
- D. 完成所有狀態的一次掃描後即終止

**答案：A**

**詳解：**
Policy Evaluation 會持續進行，直到 $\Delta < \theta$ 為止。

---

#### 112. Monte Carlo 方法屬於哪一類別？ （來源題號：12）

- A. Model-Based 方法
- B. Model-Free 方法
- C. Dynamic Programming 方法
- D. Exact Planning 方法

**答案：B**

**詳解：**
教材明確指出：「Monte Carlo (MC) is a Model Free method, It does not require complete knowledge of the environment.」它不需要知道環境的轉移機率 $p(s'|s,a)$，而是透過實際與環境互動的樣本來估計 Q 值。

---

#### 113. Monte Carlo 方法的基本概念是？ （來源題號：13）

- A. 利用 Bellman 方程式遞迴更新價值函數
- B. 對每個狀態-動作對的樣本回報取平均
- C. 使用深度神經網路逼近 Q 函數
- D. 對每個狀態直接求解線性方程組

**答案：B**

**詳解：**
Monte Carlo 方法是「averaging sample returns for each state-action pair」，透過大量的 Episode 樣本，對 $Q(s, a)$ 進行估計。不需要環境模型，只需真實或模擬的交互經驗。

---

#### 114. 在非穩態（Non-stationary）問題中，Monte Carlo 對 $V$ 的更新公式是？ （來源題號：14）

- A. $V$S_t$\leftarrow V$S_t$+ \gamma[G_t - V$S_t$]$
- B. $V$S_t$\leftarrow \alpha \cdot G_t$
- C. $V$S_t$\leftarrow V$S_t$+ \alpha[G_t - V$S_t$]$
- D. $V$S_t$\leftarrow \max_a Q$S_t, a$$

**答案：C**

**詳解：**
非穩態問題中的 Monte Carlo 更新為 $V(S_t) \leftarrow V(S_t) + \alpha [G_t - V(S_t)]$，其中 $\alpha$ 控制對新資訊的信任程度。

---

#### 115. SARSA 的名稱由來是？ （來源題號：15）

- A. State-Action-Reward-State-Agent
- B. State-Action-Reward-State-Action
- C. Sequence-Action-Return-State-Action
- D. State-Algorithm-Reward-Sampling-Action

**答案：B**

**詳解：**
SARSA 全名是「State-Action-Reward-State-Action」，名稱反映了其更新規則所用到的五個元素：$$
S_t, A_t, R_{t+1}, S_{t+1}, A_{t+1}
$$
，即「當前狀態→動作→獎勵→下一狀態→下一動作」的序列。

---

#### 116. SARSA 是 On-policy 還是 Off-policy 方法？ （來源題號：16）

- A. Off-policy
- B. On-policy
- C. 兩者都是
- D. 取決於 $\epsilon$ 的值

**答案：B**

**詳解：**
SARSA 是 on-policy 方法，因為更新時使用的 $a_{t+1}$ 是策略 $\pi$ 實際選出的下一個動作。

---

#### 117. Temporal Difference（TD）方法的核心優點是？ （來源題號：17）

- A. 必須等待完整 Episode 結束才能更新
- B. 可直接從原始經驗學習，不需環境模型
- C. 能保證收斂到全局最優解
- D. 每次更新都需要完整的狀態轉移矩陣

**答案：B**

**詳解：**
「TD methods learn directly from raw experience without a model of the environment's dynamics.」TD 方法不需要環境的完整知識，也不需要等待 Episode 結束（不像 Monte Carlo），可以進行 online、incremental 更新。

---

#### 118. TD 方法的 Value Function 更新公式是？ （來源題號：18）

- A. $V$S_t$\leftarrow V$S_t$+ \alpha[G_t - V$S_t$]$
- B. $V$S_t$\leftarrow V$S_t$+ \alpha[R_{t+1} + \gamma V$S_{t+1}$- V$S_t$]$
- C. $V$S_t$\leftarrow R_{t+1} + \gamma V$S_{t+1}$$
- D. $V$S_t$\leftarrow \max_a Q$S_t, a$$

**答案：B**

**詳解：**
TD 更新公式為 $V(S_t) \leftarrow V(S_t) + \alpha [R_{t+1} + \gamma V(S_{t+1}) - V(S_t)]$。

---

### 中等

#### 119. Bellman 方程式（Value Function 版本）的正確展開形式是？ （來源題號：19）

- A. $V_\pi(s) = \sum_a \pi(a|s) \sum_{s',r} p(s',r|s,a)[r + V_\pi(s')]$
- B. $V_\pi(s) = \sum_a \pi(a|s) \sum_{s',r} p(s',r|s,a)[r + \gamma V_\pi(s')]$
- C. $V_\pi(s) = \max_a \sum_{s',r} p(s',r|s,a)[r + \gamma V_\pi(s')]$
- D. $V_\pi(s) = \sum_{s',r} p(s',r|s,a)[r + \gamma V_\pi(s')]$

**答案：B**

**詳解：**
Bellman Equation（Value Function）為 $$V_\pi(s)=\sum_a \pi(a|s)\sum_{s',r}p(s',r|s,a)[r+\gamma V_\pi(s')]$$ 其中要對所有動作依照 $\pi(a|s)$ 加權。

---

#### 120. Bellman 方程式（Q Function 版本）展開後等於？ （來源題號：20）

- A. $q_\pi(s,a) = \sum_{s',r} p(s',r|s,a)[r + \gamma \max_{a'} q_\pi(s',a')]$
- B. $q_\pi(s,a) = \sum_{s',r} p(s',r|s,a)[r + \gamma V_\pi(s')]$
- C. $q_\pi(s,a) = \pi(a|s) \sum_{s',r} p(s',r|s,a)[r + \gamma V_\pi(s')]$
- D. $q_\pi(s,a) = \sum_a \pi(a|s)[r + \gamma V_\pi(s')]$

**答案：B**

**詳解：**
Q Function 的 Bellman 方程式為 $$q_\pi(s,a)=\sum_{s',r}p(s',r|s,a)[r+\gamma V_\pi(s')]$$，由於動作 $a$ 已經固定，因此不需要再對 $\pi(a|s)$ 加權。

---

#### 121. Policy Improvement 步驟中，如何更新策略 $\pi(s)$？ （來源題號：21）

- A. $\pi(s) \leftarrow \arg\min_a \sum_{s',r} p(s',r|s,a)[r + \gamma V(s')]$
- B. $\pi(s) \leftarrow \arg\max_a \sum_{s',r} p(s',r|s,a)[r + \gamma V(s')]$
- C. $\pi(s) \leftarrow \arg\max_a Q(s, a) \cdot \pi(a|s)$
- D. $\pi(s) \leftarrow \arg\max_a V(s')$

**答案：B**

**詳解：**
Policy Improvement 對每個狀態 $s(，選擇能最大化期望回報的動作：)$\pi(s) \leftarrow \arg\max_a \sum_{s',r} p(s',r|s,a)[r + \gamma V(s')]$$
這是 Greedy 策略改進，確保新策略不劣於舊策略（Policy Improvement Theorem）。

---

#### 122. Policy Iteration 的終止條件是什麼？ （來源題號：22）

- A. $V(s)$ 對所有狀態完全不再改變
- B. Policy Evaluation 的迴圈達到最大迭代次數
- C. Policy Improvement 後，`policy-stable = true`（新舊策略完全相同）
- D. 折扣獎勵總和超過某個閾值

**答案：C**

**詳解：**
Policy Iteration 在 Policy Improvement 步驟後，檢查 `policy-stable` 旗標。若所有狀態 $s(的 `old-action = π$s)`（即策略沒有改變），則 `policy-stable = true`，演算法終止並輸出$V \approx V^*$、$\pi \approx \pi^*$；否則返回 Policy Evaluation 繼續迭代。

---

#### 123. Value Iteration 與 Policy Iteration 的主要差異是？ （來源題號：23）

- A. Value Iteration 需要完整的環境模型，Policy Iteration 不需要
- B. Value Iteration 將 Policy Improvement 和截斷的 Policy Evaluation 合併為一步
- C. Value Iteration 使用 Q 函數更新，Policy Iteration 使用 V 函數更新
- D. Policy Iteration 每次更新只掃描一個狀態，Value Iteration 掃描所有狀態

**答案：B**

**詳解：**
教材指出：「We can avoid to wait until V(s) has converged and instead do policy improvement and truncated policy evaluation step in one operation.」Value Iteration 在每次掃描時直接取 max（Greedy），相當於只做一步 Policy Evaluation 就立即 Improve，效率更高，不需等待完整收斂。

---

#### 124. Value Iteration 的 $V(s)$ 更新公式是？ （來源題號：24）

- A. $V(s) \leftarrow \sum_a \pi(a|s) \sum_{s',r} p(s',r|s,a)[r + \gamma V(s')]$
- B. $V(s) \leftarrow \max_a \sum_{s',r} p(s',r|s,a)[r + \gamma V(s')]$
- C. $V(s) \leftarrow \arg\max_a \sum_{s',r} p(s',r|s,a)[r + \gamma V(s')]$
- D. $V(s) \leftarrow R_{t+1} + \gamma V$S_{t+1}$$

**答案：B**

**詳解：**
Value Iteration 的更新式為 $$V(s) \leftarrow \max_a \sum_{s',r} p(s',r|s,a)[r+\gamma V(s')]$$，它直接取最大值，因此同時帶有 policy improvement 的效果。

---

#### 125. SARSA 的更新規則是？ （來源題號：25）

- A. $Q$s_t, a_t$\leftarrow Q$s_t, a_t$+ \alpha[r_t + \gamma \max_{a'} Q$s_{t+1}, a'$- Q$s_t, a_t$]$
- B. $Q$s_t, a_t$\leftarrow Q$s_t, a_t$+ \alpha[r_t + \gamma Q$s_{t+1}, a_{t+1}$- Q$s_t, a_t$]$
- C. $Q$s_t, a_t$\leftarrow r_t + \gamma Q$s_{t+1}, a_{t+1}$$
- D. $Q$s_t, a_t$\leftarrow Q$s_t, a_t$+ \alpha[G_t - Q$s_t, a_t$]$

**答案：B**

**詳解：**
SARSA 的更新規則為 $Q(s_t,a_t) \leftarrow Q(s_t,a_t)+\alpha[r_t+\gamma Q(s_{t+1},a_{t+1})-Q(s_t,a_t)]$，關鍵是使用實際執行的下一個動作 $a_{t+1}$。

---

#### 126. Q-Learning 與 SARSA 最根本的差異是什麼？ （來源題號：26）

- A. Q-Learning 使用完整回報 $G_t$，SARSA 使用單步 TD 估計
- B. Q-Learning 更新時使用 $\max_{a'} Q(s', a')$，SARSA 使用實際執行的 $Q(s', a')$
- C. Q-Learning 是 on-policy，SARSA 是 off-policy
- D. Q-Learning 需要環境模型，SARSA 不需要

**答案：B**

**詳解：**
Q-Learning 使用 $\max_{a'}Q(s',a')$，與當前策略無關，因此是 off-policy；SARSA 使用實際選出的 $a'$，因此是 on-policy。

---

#### 127. n-step SARSA 的 n-step Q-Return $q_t^{(n)}$ 定義為？ （來源題號：27）

- A. $q_t^{(n)} = R_{t+1} + \gamma R_{t+2} + \ldots + \gamma^{n-1} R_{t+n} + \gamma^n Q$S_{t+n}$$
- B. $q_t^{(n)} = \sum_{k=0}^{n} \gamma^k R_{t+k+1}$
- C. $q_t^{(n)} = R_{t+1} + \gamma^n Q$S_{t+n}$$
- D. $q_t^{(n)} = \gamma^n G_t$

**答案：A**

**詳解：**
n-step Q-Return 的定義為 $q_t^{(n)} = R_{t+1}+\gamma R_{t+2}+\cdots+\gamma^{n-1}R_{t+n}+\gamma^nQ(S_{t+n})$。

---

#### 128. Forward View Sarsa($\lambda$) 的 $q_t^\lambda$ 定義是？ （來源題號：28）

- A. $q_t^\lambda = \lambda \sum_{n=1}^{\infty} (1-\lambda)^{n-1} q_t^{(n)}$
- B. $q_t^\lambda = (1-\lambda) \sum_{n=1}^{\infty} \lambda^{n-1} q_t^{(n)}$
- C. $q_t^\lambda = \sum_{n=1}^{\infty} \lambda^n q_t^{(n)}$
- D. $q_t^\lambda = (1-\lambda) q_t^{(1)} + \lambda q_t^{(\infty)}$

**答案：B**

**詳解：**
Forward View Sarsa($\lambda$) 的 $\lambda$-return 為 $q_t^\lambda=(1-\lambda)\sum_{n=1}^{\infty}\lambda^{n-1}q_t^{(n)}$。

---

#### 129. Deep Q-Learning（DQN）的損失函數 $L_i(\theta_i)$ 中，Target 的計算方式是？ （來源題號：29）

- A. $r + \gamma \max_a Q(s', a'; \theta_i)$（使用當前網路參數）
- B. $r + \gamma \max_a Q(s', a'; \theta_{i-1})$（使用前一版網路參數）
- C. $r + \gamma \sum_a \pi(a|s') Q(s', a'; \theta_{i-1})$
- D. $G_t$（完整的 Monte Carlo 回報）

**答案：B**

**詳解：**
DQN 的 loss 中，target 會使用 $r + \gamma \max_{a'} Q(s', a'; \theta_{i-1})$，也就是上一版或 target network 的估計。

---

#### 130. DQN 中「Experience Replay」（$U(D)$）的主要用途是？ （來源題號：30）

- A. 增加 Q 函數的更新頻率
- B. 打破訓練樣本之間的時序相關性，提升訓練穩定性
- C. 確保每個狀態至少被訪問一次
- D. 取代神經網路的反向傳播算法

**答案：B**

**詳解：**
Experience Replay 會把 transition $(s,a,r,s')$ 存入 replay memory $D$，訓練時再從中隨機取樣 minibatch。

---

#### 131. 在 DQN 演算法中，$\epsilon$-greedy 策略的作用是？ （來源題號：31）

- A. 確保 Q 網路的梯度更新穩定
- B. 以機率 $\epsilon(隨機選動作、以機率)1-\epsilon$ 選 greedy 動作，平衡探索與利用
- C. 當 Q 值相同時，隨機選擇動作
- D. 決定是否要將 transition 存入 replay memory

**答案：B**

**詳解：**
$\epsilon$-greedy 表示以機率 $\epsilon$ 隨機選動作，以機率 $1-\epsilon$ 選擇使 $Q(s,a;\theta)$ 最大的動作。

---

#### 132. 在 Policy Iteration 的 Policy Evaluation 步驟中，$V(s)$ 的更新公式是？ （來源題號：32）

- A. $V(s) \leftarrow \max_a \sum_{s',r} p(s',r|s,a)[r + \gamma V(s')]$
- B. $V(s) \leftarrow \sum_a \pi(a|s) \sum_{s',r} p(s',r|s,a)[r + \gamma V(s')]$
- C. $V(s) \leftarrow R_{t+1} + \gamma V$S_{t+1}$$
- D. $V(s) \leftarrow \arg\max_a Q(s, a)$

**答案：B**

**詳解：**
Policy Evaluation 在固定策略 $\pi$ 下使用 Bellman expectation equation 來更新 $V(s)$。

---

#### 133. 折扣因子 $\gamma = 0$ 時，Agent 的行為特性是？ （來源題號：33）

- A. Agent 只考慮無限遠的未來獎勵
- B. Agent 只考慮即時獎勵 $R_{t+1}$，完全不關心未來
- C. Agent 平均考慮所有未來獎勵
- D. 演算法無法收斂

**答案：B**

**詳解：**
當 $\gamma = 0$，$G_t = \sum_{k=0}^H \gamma^k r_{t+k+1} = r_{t+1}$，即總回報只等於即時獎勵，未來的獎勵全部被折扣到 0。Agent 變得完全「短視」（myopic），只最大化眼前的獎勵。當 $\gamma \to 1$，Agent 則越來越重視長期回報。

---

#### 134. Sarsa($\lambda$) 演算法（Algorithm 4）中，使用的策略是哪種？ （來源題號：34）

- A. 純 Greedy 策略
- B. Softmax 策略
- C. $\epsilon$-greedy 策略
- D. 隨機均勻策略

**答案：C**

**詳解：**
Sarsa($\lambda$) 演算法中常用由 Q 導出的 $\epsilon$-greedy 策略。

---

#### 135. 在 Monte Carlo First-visit 演算法中，如何計算 $Q(s, a)$？ （來源題號：35）

- A. 使用 Bellman 方程式遞迴計算
- B. 取每個 episode 中 $(s, a)$ 首次出現後的回報，對所有 episode 平均
- C. 取每個 episode 中 $(s, a)$ 所有出現後的回報之最大值
- D. 使用 TD 誤差進行增量更新

**答案：B**

**詳解：**
Monte Carlo First-visit 會取每個 episode 中 $(s,a)$ 第一次出現後的 return $G$，再對 $\mathrm{Returns}(s,a)$ 做平均來估計 $Q(s,a)$。

---

#### 136. 為什麼 Dynamic Programming 方法能找到最優策略？ （來源題號：36）

- A. 因為它使用神經網路進行函數逼近
- B. 因為它利用 V 和 Q 函數的子問題結構（Subproblem Structure）
- C. 因為它不需要任何環境知識
- D. 因為它透過隨機探索所有可能路徑

**答案：B**

**詳解：**
教材指出：「Taking advantages of the subproblem structure of the V and Q function we can find the optimal policy by just planning.」Bellman 方程式揭示了 RL 問題的最優子結構（Optimal Substructure），大問題的解可以分解為子問題，這是 DP 能有效求解的關鍵。

---

#### 137. 下列關於 Monte Carlo 與 TD 方法的比較，何者正確？ （來源題號：37）

- A. Monte Carlo 可以 online 更新（每步更新），TD 需要等 episode 結束
- B. TD 可以 online 更新，Monte Carlo 需要等 episode 結束後才能計算回報
- C. 兩者都需要等 episode 結束才能更新
- D. 兩者都能在每一步更新，沒有差異

**答案：B**

**詳解：**
Monte Carlo 需要等完整 episode 才能得到 $G_t$；TD 則使用 $R_{t+1}+\gamma V(S_{t+1})$，因此可以每一步即時更新。

---

#### 138. 在 DQN 中，Terminal State 的 $y_j$ 如何設定？ （來源題號：38）

- A. $y_j = r_j + \gamma \max_{a'} Q(s_j', a'; \theta)$
- B. $y_j = \gamma \max_{a'} Q(s_j', a'; \theta)$
- C. $y_j = r_j$
- D. $y_j = 0$

**答案：C**

**詳解：**
若 $s'_j$ 是 terminal state，則 DQN 的目標值直接設為 $y_j = r_j$。

---

### 困難

#### 139. Bellman Optimality Equation 隱含了什麼重要性質，使得 DP 可以高效求解 RL 問題？ （來源題號：39）

- A. RL 問題可以轉化為線性規劃問題
- B. 最優 Value Function 滿足遞迴關係，具有 Optimal Substructure 和 Overlapping Subproblems
- C. 狀態空間可以被壓縮為多項式大小
- D. 環境的隨機性可以被完全消除

**答案：B**

**詳解：**
Bellman Optimality Equation $V^*(s) = \max_a \sum_{s',r} p(s',r|s,a)[r + \gamma V^*(s')]$具有兩個關鍵性質：$1) **Optimal Substructure**：最優策略的子策略也是最優的；(2$**Overlapping Subproblems**：不同狀態的子問題相互重疊（$V^*(s')$ 可被重複使用）。這兩個性質正是 DP 能夠高效求解的充要條件。

---

#### 140. 比較 Policy Iteration 和 Value Iteration 的計算複雜度，哪個敘述最準確？ （來源題號：40）

- A. Policy Iteration 每次迭代更快，但需要更多次迭代才能收斂
- B. Value Iteration 每次迭代更快（每步直接取 max），但兩者最終迭代次數相當
- C. Value Iteration 每次迭代需要更多計算，但通常收斂所需的外層迭代次數較少
- D. Policy Iteration 通常比 Value Iteration 在更少的迭代次數內收斂，儘管每次迭代更昂貴

**答案：D**

**詳解：**
Policy Iteration 每次外層迭代包含完整的 Policy Evaluation（需多次掃描直到收斂）+ Policy Improvement，計算量大；但由於每次都做完整評估，策略改進更「精準」，通常外層迭代次數很少。Value Iteration 每次只做一步截斷評估（更快），但需要更多外層迭代才能收斂。兩者各有優劣，在實踐中 Policy Iteration 常常用更少次（但更昂貴的）迭代收斂。

---

#### 141. 在 Sarsa($\lambda$) 中，$\lambda$ 的值如何影響算法行為？請分析 $\lambda = 0$ 和 $\lambda = 1$ 的極端情況。 （來源題號：41）

- A. $\lambda = 0$ 等於 TD(0)（一步 SARSA），$\lambda = 1$ 等於 Monte Carlo
- B. $\lambda = 0$ 等於 Monte Carlo，$\lambda = 1$ 等於 TD(0)
- C. $\lambda = 0$ 完全不更新 Q 函數，$\lambda = 1$ 取所有 n-step 的平均
- D. $\lambda$ 只影響學習率，不影響 n-step 範圍

**答案：A**

**詳解：**
分析 Forward View Sarsa($\lambda$)：
$$
q_t^\lambda = (1-\lambda) \sum_{n=1}^{\infty} \lambda^{n-1} q_t^{(n)}
$$
- **$\lambda = 0$**：$q_t^\lambda = q_t^{(1)}$，也就是只有 1-step return，退化為 TD(0)，即普通 SARSA。
- **$\lambda = 1$**：在有限 episode 中可視為完整的 Monte Carlo return。
- 中間值的 $\lambda$ 會在 TD 和 MC 之間做插值。

---

#### 142. 為什麼 DQN 使用過去的參數 $\theta_{i-1}$ 作為 Target，而不是當前參數 $\theta_i$？ （來源題號：42）

- A. 降低計算複雜度，避免每步都需要更新 Target
- B. 避免 Prediction 和 Target 同時變動導致訓練不穩定（moving target 問題）
- C. 因為 $\theta_{i-1}$ 的準確度更高
- D. 使損失函數變成凸函數，確保梯度下降收斂

**答案：B**

**詳解：**
若 Target 和 Prediction 使用相同參數，更新 $\theta$ 時會同時改變 Target 值，造成 moving target 問題，讓訓練非常不穩定。DQN 使用固定一段時間的 $\theta_{i-1}$ 作為 Target，可讓學習訊號更穩定。

---

#### 143. 下列哪個情況下，Bellman Equation 的遞迴展開會出現問題？ （來源題號：43）

- A. 當折扣因子 $\gamma = 1$且 Horizon$H = \infty$（無限水平、無折扣的 continuing tasks）
- B. 當狀態空間 $|S|$ 很大時
- C. 當動作空間是連續的
- D. 當獎勵函數是隨機的

**答案：A**

**詳解：**
當 $\gamma = 1$ 且 $H = \infty$ 時，$G_t = \sum_{k=0}^{\infty} r_{t+k+1}$ 可能發散。Bellman Equation 的收斂性依賴 $\gamma < 1$ 或有限 horizon $H < \infty$。當 $\gamma < 1$ 時，幾何級數 $\sum_{k=0}^{\infty} \gamma^k = \frac{1}{1-\gamma}$ 才會收斂。

---

#### 144. 分析 Q-Learning（Algorithm 5）與 SARSA（Algorithm 4）在危險環境（Cliff Walking）中的差異行為： （來源題號：44）

- A. Q-Learning 學到最短路徑（冒險走懸崖邊），SARSA 學到較安全但較長的路徑
- B. 兩者學到完全相同的策略
- C. SARSA 學到最短路徑，Q-Learning 學到較安全的路徑
- D. 兩者都無法在 Cliff Walking 問題中收斂

**答案：A**

**詳解：**
這是經典的 Cliff Walking 例子。Q-Learning 學習的是最優策略的 Q 值（使用 $\max_{a'}$），不考慮當前 $\epsilon$-greedy 策略的隨機性，因此會偏向懸崖邊的最短路徑。SARSA 會把 $\epsilon$-greedy 的探索風險也考慮進去，所以通常學到更保守、較安全的路徑。

---

#### 145. 在 DQN 的損失函數中，$U(D)$ 代表從 replay memory 均勻採樣。若改用 Prioritized Experience Replay，其核心思想是？ （來源題號：45）

- A. 只保留最新的 N 個 transitions
- B. 根據 TD 誤差的大小決定採樣機率，TD 誤差越大的 transition 被採樣的機率越高
- C. 完全隨機地捨棄舊的 transitions
- D. 確保每個 transition 只被使用一次

**答案：B**

**詳解：**
均勻的 $U(D)$對所有 transitions 平等對待，但有些 transitions（TD 誤差大的）提供更多學習訊息。Prioritized Experience Replay 根據 TD 誤差$|r + \gamma \max_{a'} Q(s', a'; \theta_{i-1}) - Q(s, a; \theta_i)|$ 的大小來決定優先採樣順序：誤差越大，代表這個 transition 越「出乎意料」，從中可以學到更多，因此給予更高的採樣優先級。這是對 DQN 的重要改進，雖然教材未直接提及，但屬於 Double DQN 等進階主題的相關概念。

---

#### 146. 考慮 MDP 的 Markov 性質：$p(s'|s, a) = Pr\{S_{t+1} = s' | S_t = s, A_t = a\}$。這個定義隱含了什麼重要假設？ （來源題號：46）

- A. 狀態空間必須是有限的
- B. 未來狀態的轉移機率只依賴當前狀態和動作，與歷史狀態無關（Markov Property）
- C. 動作空間必須是離散的
- D. 環境的轉移必須是確定性的（Deterministic）

**答案：B**

**詳解：**
MDP 的核心是 **Markov Property**：$Pr\{S_{t+1} = s' \mid S_t, A_t, S_{t-1}, A_{t-1}, \ldots\} = Pr\{S_{t+1} = s' \mid S_t, A_t\}$。即給定當前狀態 $S_t$ 和動作 $A_t$，過去的歷史不提供任何額外資訊。若環境不滿足 Markov 性質，則需要用 POMDP 等延伸框架。

---

#### 147. 在 n-step SARSA 中，若 $n=1$ 和 $n=\infty$ 分別對應什麼方法？$n$ 的選擇如何影響 Bias-Variance Tradeoff？ （來源題號：47）

- A. $n=1$ 對應 MC；$n=\infty$ 對應 TD；較大的 $n$ 降低 Bias 但增加 Variance
- B. $n=1$ 對應 TD(SARSA)；$n=\infty$ 對應 MC；較大的 $n$ 降低 Bias 但增加 Variance
- C. $n=1$ 對應 TD(SARSA)；$n=\infty$ 對應 MC；較大的 $n$ 降低 Variance 但增加 Bias
- D. $n$ 的大小不影響 Bias-Variance Tradeoff

**答案：B**

**詳解：**
n-step Q-return 為
$$
q_t^{(n)} = R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{n-1} R_{t+n} + \gamma^n Q(S_{t+n})
$$
- $n=1$ 時，退化為 1-step TD，也就是 SARSA。
- $n=\infty$ 時，退化為 Monte Carlo。
較大的 $n$ 通常會降低 Bias，但提高 Variance。

---

#### 148. Double DQN 旨在解決標準 DQN 的什麼問題？ （來源題號：48）

- A. 解決 replay memory 容量不足的問題
- B. 解決 Q 值被高估（Overestimation）的問題，透過分離動作選擇和 Q 值估計
- C. 解決探索不足（Insufficient Exploration）的問題
- D. 解決連續動作空間無法處理的問題

**答案：B**

**詳解：**
標準 DQN 的 target 為 $r + \gamma \max_{a'} Q(s', a'; \theta_{i-1})$，會用同一個估計同時做動作選擇與價值評估，因此容易高估。Double DQN 的改進是：先用當前網路選出 $a^* = \arg\max_a Q(s', a; \theta)$，再用 target network 評估 $Q(s', a^*; \theta')$，藉此降低 overestimation。

---

#### 149. 考慮 Bellman Optimality Equation 的不動點性質（Fixed Point Property）。如果 $V^*$ 滿足：$V^*(s) = \max_a \sum_{s',r} p(s',r|s,a)[r + \gamma V^*(s')]$，這個方程式為何保證唯一解存在？ （來源題號：49）

- A. 因為狀態空間有限，可以枚舉所有可能的 V
- B. Bellman Optimality Operator 是壓縮映射（Contraction Mapping），在 $\gamma < 1$ 時保證唯一不動點
- C. 最優策略是唯一的，因此對應唯一的 $V^*$
- D. 因為獎勵函數有界，所以 V 函數必然收斂

**答案：B**

**詳解：**
定義 Bellman optimality operator 為 $(TV)(s) = \max_a \sum_{s',r} p(s',r|s,a)[r + \gamma V(s')]$。當 $\gamma < 1$ 時，$T$ 在 $\sup$-norm 下是 contraction mapping：$\|TV - TU\|_\infty \leq \gamma \|V-U\|_\infty$。因此依 Banach fixed-point theorem，$T$ 有唯一不動點，也就是 $V^*$。

---

#### 150. 綜合比較題：請分析 Dynamic Programming、Monte Carlo、Temporal Difference 三大方法在以下維度的差異：(A) 是否需要環境模型、(B) 是否需要完整 Episode、(C) 是否使用 Bootstrap。哪個選項正確描述了三者的差異？ （來源題號：50）

- A. DP（需模型、不需完整 Episode、用 Bootstrap）；MC（不需模型、需完整 Episode、不用 Bootstrap）；TD（不需模型、不需完整 Episode、用 Bootstrap）
- B. DP（需模型、需完整 Episode、用 Bootstrap）；MC（不需模型、需完整 Episode、不用 Bootstrap）；TD（不需模型、不需完整 Episode、用 Bootstrap）
- C. DP（需模型、不需完整 Episode、用 Bootstrap）；MC（需模型、需完整 Episode、不用 Bootstrap）；TD（不需模型、不需完整 Episode、用 Bootstrap）
- D. DP（需模型、不需完整 Episode、不用 Bootstrap）；MC（不需模型、需完整 Episode、用 Bootstrap）；TD（不需模型、不需完整 Episode、用 Bootstrap）

**答案：A**

**詳解：**
三大方法的完整對比：

| 方法 | 需要環境模型 | 需要完整 Episode | 使用 Bootstrap |
|---|---|---|---|
| DP | 是 | 否 | 是 |
| MC | 否 | 是 | 否 |
| TD | 否 | 否 | 是 |

Bootstrap 指用目前的 value estimate 來更新自己，而不是等完整真實回報。

---
