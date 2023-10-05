import json

roman_to_str = {"I": "Math_Logic", "II": "Sets_and_Topology", "III": "Algebra", "IV": "Number_Theory", "V": "Groups_and_Rep",
                "VI": "Alg_Geometry", "VII": "Geometry", "VIII": "Diff_Geometry", "IX": "Topology", "X": "Analysis",
                "XI": "Complex_An", "XII": "Func_An", "XIII": "Diff_Eqns", "XIV": "Spec_Func", "XV": "Num_An",
                "XVI": "Appl_An", "XVII": "Prob_Theory", "XVIII": "Stats", "XIX": "Disc_Math", 
                "XX": "Info_Math", "XXI": "Opt_Theory", "XXII": "Mech_Phys", "XXIII": "Hist_Math"}

number_to_str = {"I":{"1": "Foundations of Mathematics","2": "Semantics of Formal Systems","3": "Formal Systems and Proofs","4": "Computable Functions","5": "Model Theory","6": "Stability Theory","7": "Nonstandard Analysis","8": "Theory of Ordinal Numbers","9": "Axiomatic Set Theory","10": "Forcing","11": "Large Cardinals","12": "Descriptive Set Theory","13": "Recursive Theory","14": "Decision Problems","15": "Theory of Degrees","16": "Constructive Ordinals","17": "Proof Theory","18": "Gödel's Incompleteness Theorems","19": "Nonstandard Models of Arithmetic","20": "Type Theory and Lambda Calculus","21": "Herbrand's Theorem and Deduction Principles","22": "Nonstandard Logic","23": "Reverse Mathematics"},
                "II":{"1": "Sets","2": "Relations","3": "Equivalence Relations","4": "Functions","5": "Axiom of Choice","6": "Cardinality","7": "Structures","8": "Permutations and Combinations","9": "Numbers","10": "Real Numbers and the Real Line","11": "Complex Numbers and the Complex Plane","12": "Order","13": "Ordinal Numbers","14": "Lattices","15": "Boolean Algebra","16": "Topological Spaces","17": "Metric Spaces","18": "Plane Regions","19": "Convergence","20": "Connectedness","21": "Dimension","22": "Uniform Spaces","23": "Uniform Convergence","24": "Categories and Functors","25": "Inductive and Projective Limits","26": "Sheaves"},
                "III":{"1": "Algebra","2": "Matrices","3": "Determinants","4": "Polynomials","5": "Algebraic Equations","6": "Fields","7": "Galois Theory","8": "Vector Spaces","9": "Tensor and Exterior Products","10": "Rings","11": "Multivariate Rings","12": "Modules","13": "Representations of Multivariate Rings","14": "Homological Algebra","15": "Hopf Algebras","16": "Commutative Rings","17": "Noetherian Rings","18": "Polynomial Rings","19": "Invariants","20": "Power Series Rings","21": "Prime Ideals and Factorization Rings","22": "Homological Algebra of Commutative Rings","23": "Excellent Rings","24": "Hensel Rings and Approximation Theorems","25": "Adherent Closure of Ideals","26": "Quadratic Forms","27": "Clifford Algebras","28": "Differential Rings","29": "Witt Vectors","30": "Valuations","31": "Adèles and Ideals","32": "Cayley Algebras","33": "Jordan Algebras"},
                "IV":{"1": "Number Theory","2": "Elementary Number Theory","3": "Continued Fractions","4": "Number-Theoretic Functions","5": "Additive Number Theory","6": "Distribution of Prime Numbers","7": "Geometry of Numbers and Approximations in Number Theory","8": "Transcendental Numbers","9": "Diophantine Equations","10": "Quadratic Number Fields","11": "Algebraic Number Theory","12": "Local Fields","13": "Class Field Theory","14": "Iwasawa Theory","15": "Algebraic K-Theory","16": "Arithmetic Geometry","17": "Fermat's Last Theorem","18": "Algebraic Groups over Number Fields","19": "Modular Forms","20": "Shimura Varieties","21": "Dirichlet Series","22": "Zeta Functions","23": "Pseudo-Homogeneous Vector Spaces"},
                "V":{"1": "Group","2": "Abelian Group","3": "Finite Group","4": "Finite Simple Group","5": "Crystallographic Group","6": "Classical Group","7": "Topological Group","8": "Compact Group","9": "Lie Group","10": "Lie Algebra","11": "Algebraic Group","12": "Symmetric Space","13": "Group Actions on Homogeneous Spaces","14": "Discrete Group","15": "Representation Theory","16": "Modular Representation","17": "Unitary Representation","18": "Infinite-Dimensional Representation","19": "Group Actions and Invariants","20": "D-module","21": "Quantum Group","22": "Infinite-Dimensional Lie Algebra"},
                "VI":{"1": "Algebraic Geometry","2": "Algebraic Curves","3": "Algebraic Surfaces, Complex Analytic Surfaces","4": "Algebraic Varieties A: Sheaves and Cohomology","5": "Algebraic Varieties B: Sheaves and Cohomology","6": "Algebraic Varieties C: Rational Maps and Resolution of Singularities","7": "Algebraic Varieties D: Fibrations and Abelian Varieties","8": "Algebraic Varieties E: Riemann-Roch and Chow Rings","9": "Algebraic Varieties F: Algebraic Spaces and Formal Schemes","10": "Algebraic Varieties G: Polarized Varieties","11": "Algebraic Varieties H: Topology and Comparison Theorems","12": "Algebraic Vector Bundles","13": "Hodge Theory","14": "Abelian Varieties","15": "Rational and Fan0 Varieties","16": "Birational Geometry","17": "Toric Varieties","18": "Intersection Theory","19": "Singularity Theory","20": "Moduli Problems"},
                "VII":{"1": "Geometry","2": "Euclidean Geometry","3": "Euclidean Space","4": "Non-Euclidean Geometry","5": "Projective Geometry","6": "Affine Geometry","7": "Conformal Geometry","8": "Erlangen Program","9": "Foundations of Geometry","10": "Construction Problems","11": "Regular Polyhedra","12": "Pi (π)","13": "Trigonometry","14": "Quadratic Curves and Surfaces","15": "Convex Sets","16": "Coordinates","17": "Vector Analysis","18": "Curves","19": "Surfaces","20": "Four-Color Problem","21": "Combinatorial Geometry"},
                "VIII":{"1": "Differential Geometry","2": "Manifold","3": "Riemannian Manifold","4": "Connection","5": "Tensor and Spinor","6": "Global Riemannian Geometry","7": "Differential Geometry of Homogeneous Spaces","8": "G-Structures and Equivalence Problems","9": "Complex Manifold","10": "Harmonic Analysis","11": "Differential Geometry of Curves and Surfaces","12": "Differential Geometry of Submanifolds","13": "Minimal Submanifolds","14": "Geometric Measure Theory","15": "Harmonic Maps","16": "Morse Theory","17": "Affine Differential Geometry","18": "Finsler Space","19": "Integral Geometry","20": "Spectral Geometry","21": "Rigidity and Geometric Group Theory","22": "Symplectic and Contact Geometry","23": "Moduli Spaces and Partial Differential Equations","24": "Special Geometry"},
                "IX":{"1": "Topology","2": "Fundamental Group","3": "Covering Spaces","4": "Degree of a Mapping","5": "Complex","6": "Homology Theory","7": "Fixed Point Theorem","8": "Homotopy Theory","9": "Fiber Bundle","10": "Cobordism Theory","11": "Characteristic Classes","12": "K-Theory","13": "Knot Theory","14": "Transformation Group","15": "Singular Points of Differentiable Maps","16": "Sheaf Theory","17": "Dynamical Systems","18": "Low-Dimensional Dynamical Systems","19": "Hyperbolic Dynamical Systems","20": "Hamiltonian Systems","21": "Bifurcation of Dynamical Systems","22": "Manifold Topology","23": "Index Theory","24": "3-Dimensional Manifolds","25": "4-Dimensional Manifolds","26": "Geometric Topology"},
                "X":{"1": "Analysis","2": "Continuous Functions","3": "Inequalities","4": "Convex Analysis","5": "Functions of Bounded Variation","6": "Differential Calculus","7": "Operational Calculus","8": "Implicit Function","9": "Elementary Functions","10": "C∞ Functions, Infinitesimal Calculus","11": "Integration","12": "Line and Surface Integrals","13": "Measure Theory","14": "Integral Calculus","15": "Invariant Measures","16": "Length and Area","17": "Fractals","18": "Series","19": "Asymptotic Series","20": "Polynomial Approximation","21": "Orthogonal Function Systems","22": "Fourier Series","23": "Fourier Transform","24": "Wavelets","25": "Harmonic Analysis, Real Analysis","26": "Quasiperiodic Functions","27": "Laplace Transform","28": "Integral Transforms","29": "Potential Theory","30": "Harmonic Functions, Superharmonic Functions","31": "Dirichlet Problem","32": "Capacity","33": "Calculus of Variations","34": "Plateau's Problem","35": "Isoperimetric Problems"},
                "XI":{"1": "Complex Analysis","2": "Holomorphic Functions","3": "Power Series","4": "Family of Holomorphic Functions","5": "Maximum Modulus Principle","6": "Boundary Behavior of Analytic Functions","7": "Univalent Functions","8": "Value Distribution Theory","9": "Complex Approximation Theory","10": "Riemann Surfaces","11": "Analytic Functions on Riemann Surfaces","12": "Complex Dynamical Systems","13": "Conformal Mapping","14": "Quasiconformal Mapping","15": "Teichmüller Space","16": "Kleinian Group","17": "Multivariable Analytic Functions","18": "Analytic Space","19": "¯∂ Equation","20": "Holomorphic Mapping","21": "Plurisubharmonic Functions","22": "CR Manifold","23": "Kernel Functions","24": "Siegel Domain","25": "Periodic Integration"},
                "XII":{"1": "Functional Analysis","2": "Hilbert Space","3": "Banach Space","4": "Ordered Linear Space","5": "Linear Topological Space","6": "Function Space","7": "Distributions (Generalized Functions)","8": "Vector-Valued Integration","9": "Linear Operators","10": "Compact Operators, Nuclear Operators","11": "Interpolation Spaces","12": "Spectral Analysis of Operators","13": "Operator Inequalities","14": "Perturbation of Linear Operators","15": "Operator Semigroups, Evolution Equations","16": "Banach Algebras","17": "C*-Algebras","18": "Function Algebras","19": "von Neumann Algebras","20": "Nonlinear Functional Analysis"},
                "XIII":{"1": "Differential Equations","2": "Initial Value Problems for Ordinary Differential Equations","3": "Boundary Value Problems for Ordinary Differential Equations","4": "Linear Ordinary Differential Equations","5": "Local Theory of Linear Ordinary Differential Equations","6": "Global Theory of Linear Ordinary Differential Equations","7": "Local Theory of Nonlinear Ordinary Differential Equations","8": "Global Theory of Nonlinear Ordinary Differential Equations","9": "Painlevé Equations","10": "Nonlinear Oscillations","11": "Nonlinear Problems","12": "Stability","13": "Invariant Integrals","14": "Difference Equations","15": "Functional Differential Equations","16": "Total Differential Equations","17": "Solution of Partial Differential Equations","18": "Quasilinear Equations, Solvability","19": "Initial Value Problems for Partial Differential Equations","20": "Partial Differential Equations in Complex Domains","21": "First-Order Partial Differential Equations","22": "Monge-Ampère Equations","23": "Elliptic Partial Differential Equations","24": "Hyperbolic Partial Differential Equations","25": "Parabolic Partial Differential Equations","26": "Mixed Type Partial Differential Equations","27": "Inequalities in Differential Equations","28": "Green's Functions, Green's Operators","29": "Integral Equations","30": "Integro-Differential Equations","31": "Special Function Equations","32": "Microlocal Analysis and Pseudodifferential Operators"},
                "XIV":{"1": "Special Functions","2": "Generating Functions","3": "Elliptic Functions","4": "Gamma Function","5": "Hypergeometric Functions","6": "Spherical Harmonics","7": "Confluent Hypergeometric Functions","8": "Bessel Functions","9": "Ellipsoidal Harmonic Functions","10": "Mathieu Functions","11": "q-Series","12": "Polylogarithm Functions","13": "Special Orthogonal Polynomials"},
                "XV":{"1": "Numerical Analysis","2": "Numerical Solutions of Linear Systems","3": "Numerical Solutions of Nonlinear Equations","4": "Numerical Eigenvalue Computation","5": "Numerical Integration Methods","6": "Numerical Solutions of Ordinary Differential Equations","7": "Numerical Solutions of Partial Differential Equations","8": "Finite Difference Methods","9": "Finite Element Methods","10": "Function Approximation Methods","11": "Certified Numerical Computations"},
                "XVI":{"1": "Mathematical Modeling","2": "Reaction-Diffusion Equations","3": "Free Boundary Problems","4": "Variational Analysis","5": "Fluid Equations","6": "Conservation Laws","7": "Nonlinear Wave and Dispersion Equations","8": "Scattering Theory","9": "Inverse Problems","10": "Viscous Solutions"},
                "XVII":{"1": "Probability Theory","2": "Probability Measure","3": "Stochastic Processes","4": "Limit Theorems in Probability Theory","5": "Markov Processes","6": "Markov Chains","7": "Brownian Motion","8": "Lévy Processes","9": "Martingales","10": "Diffusion Processes","11": "Stochastic Differential Equations","12": "Martingale Analysis","13": "Measure-Valued Stochastic Processes","14": "Gaussian Processes","15": "Stationary Processes","16": "Ergodic Theory","17": "Probability Control and Filtering","18": "Probabilistic Methods in Statistical Physics"},
                "XVIII":{"1": "Statistics","2": "Statistical Models and Inference","3": "Statistical Quantities and Sample Distributions","4": "Statistical Estimation","5": "Statistical Hypothesis Testing","6": "Multivariate Analysis","7": "Robust Nonparametric Methods","8": "Experimental Design","9": "Sampling Methods","10": "Actuarial Mathematics","11": "Time Series Analysis","12": "Inference for Stochastic Processes","13": "Statistical Computing","14": "Information Geometry"},
                "XIX":{"1": "Discrete Mathematics and Combinatorics","2": "Graph Theory","3": "Enumerative Combinatorics","4": "Matroids","5": "Design Theory","6": "Discrete Geometry","7": "Extremal Set Theory","8": "Algebraic Combinatorics"},
                "XX":{"1": "Mathematics in Computer Science","2": "Formal Language Theory and Automata","3": "Computational Complexity Theory","4": "Information Theory","5": "Coding Theory","6": "Cryptography","7": "Computer Algebra","8": "Computational Geometry","9": "Randomness and Monte Carlo Methods"},
                "XXI":{"1": "Mathematical Programming","2": "Linear Programming","3": "Nonlinear Programming","4": "Semidefinite Programming","5": "Global Optimization","6": "Network Flow","7": "Discrete Convex Analysis","8": "Integer Programming","9": "Combinatorial Optimization","10": "Dynamic Programming","11": "Stochastic Programming","12": "Game Theory","13": "Complementarity Problem","14": "Control Theory","15": "Operations Research","16": "Portfolio Theory","17": "Markov Decision Process"},
                "XXII":{"1": "Units and Dimensions","2": "Dimensional Analysis","3": "Variational Principles in Physics","4": "Classical Mechanics","5": "Celestial Mechanics","6": "Astrophysics","7": "Three-Body Problem","8": "Fluid Mechanics","9": "Plasma Physics","10": "Turbulence","11": "Complex Systems","12": "Phase Transitions","13": "Oscillations and Waves","14": "Geometrical Optics","15": "Electromagnetism","16": "Circuits","17": "Thermodynamics","18": "Statistical Mechanics","19": "Theory of Relativity","20": "Unified Field Theories","21": "Quantum Mechanics","22": "Lorentz Group","23": "Lie Algebras","24": "Second Quantization","25": "Field Theory","26": "S-Matrix","27": "Feynman Integrals","28": "Particle Physics","29": "Renormalization Group","30": "Integrable Models","31": "Solitons","32": "Conformal Field Theory","33": "Approximation Methods in Physics"},
                "XXIII":{"1": "Egyptian and Babylonian Mathematics","2": "Greek and Roman Mathematics","3": "Mathematics in Medieval Europe","4": "Arabic Mathematics","5": "Indian Mathematics","6": "Chinese Mathematics","7": "Japanese Mathematics (Wagaku)","8": "Mathematics in the Renaissance","9": "Mathematics in the 17th Century","10": "Mathematics in the 18th Century","11": "Mathematics in the 19th Century"}}

def split_roman_and_num(s):
    # ローマ数字とアラビア数字の対応表を辞書型で作る
    roman_dict = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
    # ローマ数字とアラビア数字の部分を空文字列に初期化する
    roman_part = ''
    num_part = ''
    # 新しい文字列の各文字についてループする
    for c in s:
        # 文字がローマ数字であれば、ローマ数字の部分に追加する
        if c in roman_dict:
            roman_part += c
        # 文字がアラビア数字であれば、アラビア数字の部分に追加する
        elif c.isdigit():
            num_part += c
        # 文字がどちらでもなければ、エラーを返す
        else:
            return 'Error: invalid character'
    # ローマ数字とアラビア数字の部分をタプルとして返す
    if num_part == '':
        return 'Error: nothing number'    
    return (roman_part, num_part)

def replace_number_to_name():
    if len(parent) >= 2:
        romanAndNum = parent[1] # "/I9/A"のI9の部分
        result = split_roman_and_num(romanAndNum)
        if result != 'Error: invalid character':
            roman, num = result
            if roman in roman_to_str:
                parent[1] = roman_to_str[roman] + num
                obj["data"]["parent"] = "/".join(parent)
            else:
                print('Invalid input: the Roman numeral does not exist')
        else:
            print(result)
    else:
        print('Invalid input: the string does not have enough elements')

graph_json = open('graph_attrs/graph_classHierar_test.json', 'r')
graph_objects = json.load(graph_json)



for obj in graph_objects["eleObjs"]:
    if obj["group"] == "nodes":
        id_slash = obj["data"]["id"]
        name = obj["data"]["name"]
        if obj["data"].get("parent"):
            parent_slash = obj["data"]["parent"]
            parent = parent_slash.split("/")
            if len(parent) >= 2:
                romanAndNum = parent[1] # "/I9/A"のI9の部分
                result = split_roman_and_num(romanAndNum)
                if result != 'Error: invalid character':
                    roman, num = result
                    if roman in roman_to_str:
                        parent[1] = roman_to_str[roman] + number_to_str[roman][num]
                        obj["data"]["parent"] = "/".join(parent)
                    else:
                        print('Invalid input: the Roman numeral does not exist')
                else:
                    print(result)
            else:
                print('Invalid input: the string does not have enough elements')

        id = id_slash.split("/")
        if len(id) >= 2:
            romanAndNum = id[1] # "/I9/A"のI9の部分
            result = split_roman_and_num(romanAndNum)
            if result != 'Error: invalid character':
                roman, num = result
                if roman in roman_to_str:
                    id[1] = roman_to_str[roman] + number_to_str[roman][num]
                    obj["data"]["id"] = "/".join(id)
                else:
                    print('Invalid input: the Roman numeral does not exist')
            else:
                print(result)
        else:
            print('Invalid input: the string does not have enough elements')

        if len(name) >= 2:
            romanAndNum = name # "/I9/A"のI9の部分
            result = split_roman_and_num(romanAndNum)
            if result != 'Error: invalid character':
                roman, num = result
                if roman in roman_to_str:
                    name = roman_to_str[roman] + number_to_str[roman][num]
                    obj["data"]["name"] = name
                else:
                    print('Invalid input: the Roman numeral does not exist')
            else:
                print(result)
        else:
            print('Invalid input: the string does not have enough elements')

for obj in graph_objects["parents"]:
    if obj["group"] == "nodes":
        id_slash = obj["data"]["id"]
        name = obj["data"]["name"]
        if obj["data"].get("parent"):
            parent_slash = obj["data"]["parent"]
            parent = parent_slash.split("/")
            if len(parent) >= 2:
                romanAndNum = parent[1] # "/I9/A"のI9の部分
                result = split_roman_and_num(romanAndNum)
                if result != 'Error: invalid character':
                    roman, num = result
                    if roman in roman_to_str:
                        parent[1] = roman_to_str[roman] + number_to_str[roman][num]
                        obj["data"]["parent"] = "/".join(parent)
                    else:
                        print('Invalid input: the Roman numeral does not exist')
                else:
                    print(result)
            else:
                print('Invalid input: the string does not have enough elements')

        id = id_slash.split("/")
        if len(id) >= 2:
            romanAndNum = id[1] # "/I9/A"のI9の部分
            result = split_roman_and_num(romanAndNum)
            if result != 'Error: invalid character':
                roman, num = result
                if roman in roman_to_str:
                    id[1] = roman_to_str[roman] + number_to_str[roman][num]
                    obj["data"]["id"] = "/".join(id)
                else:
                    print('Invalid input: the Roman numeral does not exist')
            else:
                print(result)
        else:
            print('Invalid input: the string does not have enough elements')

        if len(name) >= 2:
            romanAndNum = name # "/I9/A"のI9の部分
            result = split_roman_and_num(romanAndNum)
            if result != 'Error: invalid character':
                roman, num = result
                if roman in roman_to_str:
                    name = roman_to_str[roman] + number_to_str[roman][num]
                    obj["data"]["name"] = name
                else:
                    print('Invalid input: the Roman numeral does not exist')
            else:
                print(result)
        else:
            print('Invalid input: the string does not have enough elements')
        

with open('graph_attrs/graph_Hierar_replace.json', 'w') as f :
    json.dump(graph_objects, f, indent=4)

print(graph_objects)