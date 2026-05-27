# Technical Report: The Gale-Shapley Stable Matching Algorithm

This technical report details the implementation, execution, and mathematical foundations of the **Gale-Shapley Algorithm** (also known as the **Deferred Acceptance Algorithm**) applied to match eight students with eight universities.

---

## 1. Introduction

The **Stable Matching Problem (SMP)** is a classic problem in economics, mathematics, and computer science. First formulated by David Gale and Lloyd Shapley in 1962, the problem asks whether it is always possible to pair two sets of equal size (e.g., students and universities, or applicants and employers) in such a way that the matches are **stable**.

A matching is defined as **unstable** if there exists any pair of elements—say, student $S$ and university $U$—such that:
1. $S$ prefers $U$ over their current assigned university.
2. $U$ prefers $S$ over their current matched student.

Such a pair $(S, U)$ is called a **blocking pair**. The Gale-Shapley algorithm guarantees that a stable matching can always be found, and it terminates in polynomial time. For their work on stable matchings and market design, Lloyd Shapley (along with Alvin Roth) was awarded the Nobel Prize in Economics in 2012.

---

## 2. Input Description

The problem instance consists of $N = 8$ students and $N = 8$ universities. Each participant has a strict order of preference over all members of the opposite set.

### 2.1 Participating Entities
- **Students**: Andreas, Maria, Giorgos, Eleni, Nikos, Sofia, Petros, Anna.
- **Universities**: MIT, Stanford, Harvard, Berkeley, Caltech, Princeton, Yale, Columbia.

### 2.2 Preference Lists

The preference lists are defined as follows (ordered from index 0 [highest preference] to index 7 [lowest preference]):

#### Students' Preference Table
| Student | 1st Choice | 2nd Choice | 3rd Choice | 4th Choice | 5th Choice | 6th Choice | 7th Choice | 8th Choice |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Andreas** | MIT | Stanford | Harvard | Berkeley | Caltech | Princeton | Yale | Columbia |
| **Maria** | Harvard | MIT | Stanford | Yale | Princeton | Berkeley | Columbia | Caltech |
| **Giorgos** | Stanford | Berkeley | MIT | Harvard | Columbia | Caltech | Princeton | Yale |
| **Eleni** | Princeton | Yale | Harvard | MIT | Stanford | Columbia | Berkeley | Caltech |
| **Nikos** | Berkeley | Stanford | MIT | Caltech | Harvard | Princeton | Yale | Columbia |
| **Sofia** | Yale | Harvard | Princeton | MIT | Stanford | Berkeley | Columbia | Caltech |
| **Petros** | Columbia | Caltech | Berkeley | Stanford | MIT | Harvard | Princeton | Yale |
| **Anna** | Caltech | Columbia | Yale | Princeton | Harvard | MIT | Stanford | Berkeley |

#### Universities' Preference Table
| University | 1st Choice | 2nd Choice | 3rd Choice | 4th Choice | 5th Choice | 6th Choice | 7th Choice | 8th Choice |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MIT** | Andreas | Maria | Giorgos | Sofia | Nikos | Eleni | Petros | Anna |
| **Stanford** | Giorgos | Andreas | Maria | Nikos | Sofia | Eleni | Anna | Petros |
| **Harvard** | Maria | Sofia | Eleni | Andreas | Giorgos | Anna | Nikos | Petros |
| **Berkeley** | Giorgos | Nikos | Andreas | Petros | Maria | Sofia | Eleni | Anna |
| **Caltech** | Anna | Petros | Nikos | Giorgos | Andreas | Maria | Sofia | Eleni |
| **Princeton** | Eleni | Sofia | Maria | Andreas | Nikos | Giorgos | Anna | Petros |
| **Yale** | Sofia | Maria | Eleni | Anna | Andreas | Giorgos | Nikos | Petros |
| **Columbia** | Petros | Anna | Maria | Giorgos | Sofia | Andreas | Nikos | Eleni |

---

## 3. Algorithm Explanation & Mechanics

The algorithm is based on a **proposer-responder** model. In this implementation, the **students are the proposers** and the **universities are the responders**. 

### 3.1 Step-by-Step Procedure
1. **Initialization**:
   - Create a queue/list of all students and mark them as "free" (unmatched).
   - Initialize all universities as free (unmatched).
   - Maintain a pointer for each student to track their next choice for proposal (starting at index 0).

2. **The Iterative Proposal Loop**:
   - While there is at least one free student $S$ who has not proposed to all universities:
     - Locate the next university $U$ on $S$'s preference list.
     - $S$ makes a proposal to $U$.
     - **Case A: $U$ is free**
       - $U$ and $S$ form a tentative match. $S$ is removed from the free students list.
     - **Case B: $U$ is already matched to another student $S_{curr}$**
       - $U$ compares $S$ with $S_{curr}$ using its preference list.
       - **Sub-case B1: $U$ prefers $S$ over $S_{curr}$**
         - The match is updated: $U$ is matched with $S$.
         - $S$ is removed from the free students list.
         - $S_{curr}$ is rejected and added back to the free students list.
       - **Sub-case B2: $U$ prefers $S_{curr}$ over $S$**
         - $S$ is rejected and remains in the free students list (to propose to their next choice in a subsequent step).

3. **Termination**:
   - The loop terminates when the free students list becomes empty (everyone is matched).

### 3.2 Mathematical Proofs of Core Properties

#### Theorem 1: The algorithm always terminates.
*Proof*: In every iteration, a student proposes to a university they have never proposed to before. Since there are $N$ students and $N$ universities, the maximum number of proposals that can ever be made is $N \times N = N^2$. Since the number of remaining possible proposals strictly decreases at each step (or every rejection), the algorithm must terminate in at most $N^2$ steps.

#### Theorem 2: The final matching is perfect (everyone is matched).
*Proof*: Suppose, by contradiction, that when the algorithm terminates, there is a student $S$ who is unmatched. Since the number of students equals the number of universities, if $S$ is unmatched, there must be some university $U$ that is also unmatched.
However, a student only remains unmatched if they have proposed to all universities and been rejected by all of them. But a university only rejects a student if it accepts another student. Once a university is matched, it never becomes unmatched; it only exchanges its partner for a preferred one. Since $U$ was never matched (by assumption), it must never have received a proposal. However, $S$ proposed to all universities, including $U$. This is a contradiction. Hence, all students and universities must be matched.

#### Theorem 3: The final matching is stable.
*Proof*: Suppose, by contradiction, that there is an instability represented by a blocking pair $(S, U)$, where $S$ is matched to $U_{curr}$ and $U$ is matched to $S_{curr}$, but:
- $S$ prefers $U$ over $U_{curr}$.
- $U$ prefers $S$ over $S_{curr}$.

Since $S$ prefers $U$ over $U_{curr}$, and the algorithm forces students to propose in descending order of preferences, $S$ must have proposed to $U$ before proposing to $U_{curr}$. 
When $S$ proposed to $U$, $U$ must have either rejected $S$ (preferring its match at the time) or accepted $S$ and subsequently rejected them for a better candidate. In either case, the university $U$ ended up with a student it prefers more than $S$. Since a university's partner can only improve in preference over the course of the algorithm, $U$ must prefer its final partner $S_{curr}$ over $S$.
This contradicts the assumption that $U$ prefers $S$ over $S_{curr}$. Thus, no blocking pair can exist, and the matching is stable.

#### Theorem 4: Proposer Optimality and Responder Pessimality.
- **Proposer-Optimal**: In a proposer-proposing Gale-Shapley matching, every proposer receives their best possible partner in *any* stable matching.
- **Responder-Pessimal**: Every responder receives their worst possible partner in *any* stable matching.
Because our script is student-proposing, the final matching is **student-optimal** and **university-pessimal**.

---

## 4. Complexity Analysis

- **Time Complexity**:
  - In the worst case, each of the $N$ students proposes to all $N$ universities. The outer loop runs at most $O(N^2)$ times.
  - Inside the loop, checking if a university is matched is $O(1)$ using a hash map/dictionary lookup.
  - Comparing preferences: Under a naive implementation, finding the index of a student in the university's preference list takes $O(N)$ time. However, this can be pre-processed to $O(1)$ by storing the rankings in a lookup table (a dictionary of student ranks for each university). In our current implementation, we use `.index()` which is $O(N)$, resulting in an overall worst-case complexity of $O(N^3)$. For $N=8$, this overhead is negligible, but for large datasets, pre-processing is recommended to achieve $O(N^2)$.
  - Thus, the theoretical time complexity is $\mathbf{O(N^2)}$ with pre-processing.

- **Space Complexity**:
  - The preference matrices take $O(N^2)$ space.
  - Auxiliary tracking structures (`matches`, `free_students`, `next_choice`) take $O(N)$ space.
  - Overall space complexity is $\mathbf{O(N^2)}$.

---

## 5. Code Structure and Implementation Details

The implementation in [gale_shapley.py](file:///Users/sajidmahmud/Downloads/Gale-Shapley-Algo/gale_shapley.py) is organized into three primary sections:

1. **Data Representation**:
   - `students` and `universities` are represented as string lists.
   - Preference lists (`student_pref` and `uni_pref`) are represented as dictionaries of lists, mapped by the entity's name.

2. **Core Subroutines**:
   - `print_preferences()`: Output helper to display preferences.
   - `prefers_new_student(university, new_student, current_student)`: Evaluates whether a university prefers the proposing student over the current match. This performs a comparison of list index lookups:
     ```python
     pref_list = uni_pref[university]
     return pref_list.index(new_student) < pref_list.index(current_student)
     ```
   - `print_matches(matches)`: Formats and displays intermediate matches during the execution steps.

3. **Gale-Shapley Engine (`gale_shapley()`)**:
   - Implements a queue-based solution utilizing `free_students = students.copy()`.
   - Uses `next_choice` to keep track of indices of proposals.
   - Tracks rejections through the `rejections` integer variable.

---

## 6. Execution Results & Analysis

When the algorithm is executed, it completes in **exactly 8 steps**, yielding a perfect matching with **0 total rejections**.

### 6.1 Final Stable Matching

The final matching is as follows:

| Student | Assigned University | Student Preference Rank | University Preference Rank |
| :--- | :--- | :---: | :---: |
| **Andreas** | MIT | 1st (MIT) | 1st (Andreas) |
| **Maria** | Harvard | 1st (Harvard) | 1st (Maria) |
| **Giorgos** | Stanford | 1st (Stanford) | 1st (Giorgos) |
| **Eleni** | Princeton | 1st (Princeton) | 1st (Eleni) |
| **Nikos** | Berkeley | 1st (Berkeley) | 2nd (Nikos) |
| **Sofia** | Yale | 1st (Yale) | 1st (Sofia) |
| **Petros** | Columbia | 1st (Columbia) | 1st (Petros) |
| **Anna** | Caltech | 1st (Caltech) | 1st (Anna) |

### 6.2 Mathematical Explanation of the Zero Rejections Result
Typically, the Gale-Shapley algorithm involves multiple proposals, rejections, and re-proposals before reaching stability. However, in this specific dataset, there are **0 rejections**. Let's examine why:
- Out of the 8 students, **7 students** (Andreas, Maria, Giorgos, Eleni, Sofia, Petros, and Anna) have their 1st choice university list them as their 1st choice student. This forms a mutual first-choice pairing, which is guaranteed to match immediately and remain stable (mutual first choices can never be disrupted since both parties are at their absolute peak preference).
- The only student without a mutual first choice is **Nikos**. Nikos's 1st choice is Berkeley. Berkeley's 1st choice is Giorgos.
- However, Giorgos's 1st choice is Stanford (not Berkeley). Since Giorgos proposes to Stanford first, he is accepted and never proposes to Berkeley.
- Thus, when Nikos proposes to Berkeley, Berkeley is unmatched and accepts Nikos immediately.
- Since all students were accepted by their 1st choices, no student ever proposes to a second choice, resulting in 0 rejections.

This represents the absolute best-case scenario for the proposing side, demonstrating **Perfect Student-Optimality**.

---

## 7. Screenshot / Execution Tracing Suggestion

To visually document the execution in a presentation or assignment submission, include the following screenshots:

1. **Figure 1 (Preference Configurations)**: A screenshot of the terminal output showing the printed `STUDENTS' PREFERENCES` and `UNIVERSITIES' PREFERENCES` tables at startup.
2. **Figure 2 (Step-by-Step Proposals)**: A screenshot of the intermediate step logs (Steps 1 through 8) highlighting the sequential proposals and the progressive matches list.
3. **Figure 3 (Final Stable Matching Report)**: A screenshot of the bottom of the execution output displaying `FINAL STABLE MATCHING`, the statement `Perfect Matching: Yes`, and the statement `Total Rejections: 0`.

---

## 8. Conclusion

The execution of the Gale-Shapley algorithm on this dataset confirms the theoretical guarantees of stable matching. By using Python's list and dictionary structures, we were able to implement the deferred acceptance logic clearly, and trace the execution path step-by-step. The zero-rejection outcome serves as a clear illustration of how highly aligned preference matrices minimize friction and yield immediate stability.
