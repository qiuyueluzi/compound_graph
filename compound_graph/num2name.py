import json

roman_to_str = {"I": "Math_Logic", "II": "Sets_and_Topology", "III": "Algebra", "IV": "Number_Theory", "V": "Groups_and_Rep",
                "VI": "Alg_Geometry", "VII": "Geometry", "VIII": "Diff_Geometry", "IX": "Topology", "X": "Analysis",
                "XI": "Complex_An", "XII": "Func_An", "XIII": "Diff_Eqns", "XIV": "Spec_Func", "XV": "Num_An",
                "XVI": "Appl_An", "XVII": "Prob_Theory", "XVIII": "Stats", "XIX": "Disc_Math", 
                "XX": "Info_Math", "XXI": "Opt_Theory", "XXII": "Mech_Phys", "XXIII": "Hist_Math"}

number_to_str = {
                "I":{"1": "Foundations_of_Mathematics","2": "Semantics_of_Formal_Systems","3": "Formal_Systems_and_Proofs","4": "Computable_Functions","5": "Model_Theory","6": "Stability_Theory","7": "Nonstandard_Analysis","8": "Theory_of_Ordinal_Numbers","9": "Axiomatic_Set_Theory","10": "Forcing","11": "Large_Cardinals","12": "Descriptive_Set_Theory","13": "Recursive_Theory","14": "Decision_Problems","15": "Theory_of_Degrees","16": "Constructive_Ordinals","17": "Proof_Theory","18": "Godels_Incompleteness_Theorems","19": "Nonstandard_Models_of_Arithmetic","20": "Type_Theory_and_Lambda_Calculus","21": "Herbrands_Theorem_and_Deduction_Principles","22": "Nonstandard_Logic","23": "Reverse_Mathematics"},
                "II":{"1": "Sets","2": "Relations","3": "Equivalence_Relations","4": "Functions","5": "Axiom_of_Choice","6": "Cardinality","7": "Structures","8": "Permutations_and_Combinations","9": "Numbers","10": "Real_Numbers_and_the_Real_Line","11": "Complex_Numbers_and_the_Complex_Plane","12": "Order","13": "Ordinal_Numbers","14": "Lattices","15": "Boolean_Algebra","16": "Topological_Spaces","17": "Metric_Spaces","18": "Plane_Regions","19": "Convergence","20": "Connectedness","21": "Dimension","22": "Uniform_Spaces","23": "Uniform_Convergence","24": "Categories_and_Functors","25": "Inductive_and_Projective_Limits","26": "Sheaves"},
                "III":{"1": "Algebra","2": "Matrices","3": "Determinants","4": "Polynomials","5": "Algebraic_Equations","6": "Fields","7": "Galois_Theory","8": "Vector_Spaces","9": "Tensor_and_Exterior_Products","10": "Rings","11": "Multivariate_Rings","12": "Modules","13": "Representations_of_Multivariate_Rings","14": "Homological_Algebra","15": "Hopf_Algebras","16": "Commutative_Rings","17": "Noetherian_Rings","18": "Polynomial_Rings","19": "Invariants","20": "Power_Series_Rings","21": "Prime_Ideals_and_Factorization_Rings","22": "Homological_Algebra_of_Commutative_Rings","23": "Excellent_Rings","24": "Hensel_Rings_and_Approximation_Theorems","25": "Adherent_Closure_of_Ideals","26": "Quadratic_Forms","27": "Clifford_Algebras","28": "Differential_Rings","29": "Witt_Vectors","30": "Valuations","31": "Adèles_and_Ideals","32": "Cayley_Algebras","33": "Jordan_Algebras"},
                "IV":{"1": "Number_Theory","2": "Elementary_Number_Theory","3": "Continued_Fractions","4": "Number-Theoretic_Functions","5": "Additive_Number_Theory","6": "Distribution_of_Prime_Numbers","7": "Geometry_of_Numbers_and_Approximations_in_Number_Theory","8": "Transcendental_Numbers","9": "Diophantine_Equations","10": "Quadratic_Number_Fields","11": "Algebraic_Number_Theory","12": "Local_Fields","13": "Class_Field_Theory","14": "Iwasawa_Theory","15": "Algebraic_K-Theory","16": "Arithmetic_Geometry","17": "Fermats_Last_Theorem","18": "Algebraic_Groups_over_Number_Fields","19": "Modular_Forms","20": "Shimura_Varieties","21": "Dirichlet_Series","22": "Zeta_Functions","23": "Pseudo-Homogeneous_Vector_Spaces"},
                "V":{"1": "Group","2": "Abelian_Group","3": "Finite_Group","4": "Finite_Simple_Group","5": "Crystallographic_Group","6": "Classical_Group","7": "Topological_Group","8": "Compact_Group","9": "Lie_Group","10": "Lie_Algebra","11": "Algebraic_Group","12": "Symmetric_Space","13": "Group_Actions_on_Homogeneous_Spaces","14": "Discrete_Group","15": "Representation_Theory","16": "Modular_Representation","17": "Unitary_Representation","18": "Infinite-Dimensional_Representation","19": "Group_Actions_and_Invariants","20": "D-module","21": "Quantum_Group","22": "Infinite-Dimensional_Lie_Algebra"},
                "VI":{"1": "Algebraic_Geometry","2": "Algebraic_Curves","3": "Algebraic_Surfaces,_Complex_Analytic_Surfaces","4": "Algebraic_Varieties_A_Sheaves_and_Cohomology","5": "Algebraic_Varieties_B_Sheaves_and_Cohomology","6": "Algebraic_Varieties_C_Rational_Maps_and_Resolution_of_Singularities","7": "Algebraic_Varieties_D_Fibrations_and_Abelian_Varieties","8": "Algebraic_Varieties_E_Riemann-Roch_and_Chow_Rings","9": "Algebraic_Varieties_F_Algebraic_Spaces_and_Formal_Schemes","10": "Algebraic_Varieties_G_Polarized_Varieties","11": "Algebraic_Varieties_H_Topology_and_Comparison_Theorems","12": "Algebraic_Vector_Bundles","13": "Hodge_Theory","14": "Abelian_Varieties","15": "Rational_and_Fan0_Varieties","16": "Birational_Geometry","17": "Toric_Varieties","18": "Intersection_Theory","19": "Singularity_Theory","20": "Moduli_Problems"},
                "VII":{"1": "Geometry","2": "Euclidean_Geometry","3": "Euclidean_Space","4": "Non-Euclidean_Geometry","5": "Projective_Geometry","6": "Affine_Geometry","7": "Conformal_Geometry","8": "Erlangen_Program","9": "Foundations_of_Geometry","10": "Construction_Problems","11": "Regular_Polyhedra","12": "Pi","13": "Trigonometry","14": "Quadratic_Curves_and_Surfaces","15": "Convex_Sets","16": "Coordinates","17": "Vector_Analysis","18": "Curves","19": "Surfaces","20": "Four-Color_Problem","21": "Combinatorial_Geometry"},
                "VIII":{"1": "Differential_Geometry","2": "Manifold","3": "Riemannian_Manifold","4": "Connection","5": "Tensor_and_Spinor","6": "Global_Riemannian_Geometry","7": "Differential_Geometry_of_Homogeneous_Spaces","8": "G-Structures_and_Equivalence_Problems","9": "Complex_Manifold","10": "Harmonic_Analysis","11": "Differential_Geometry_of_Curves_and_Surfaces","12": "Differential_Geometry_of_Submanifolds","13": "Minimal_Submanifolds","14": "Geometric_Measure_Theory","15": "Harmonic_Maps","16": "Morse_Theory","17": "Affine_Differential_Geometry","18": "Finsler_Space","19": "Integral_Geometry","20": "Spectral_Geometry","21": "Rigidity_and_Geometric_Group_Theory","22": "Symplectic_and_Contact_Geometry","23": "Moduli_Spaces_and_Partial_Differential_Equations","24": "Special_Geometry"},
                "IX":{"1": "Topology","2": "Fundamental_Group","3": "Covering_Spaces","4": "Degree_of_a_Mapping","5": "Complex","6": "Homology_Theory","7": "Fixed_Point_Theorem","8": "Homotopy_Theory","9": "Fiber_Bundle","10": "Cobordism_Theory","11": "Characteristic_Classes","12": "K-Theory","13": "Knot_Theory","14": "Transformation_Group","15": "Singular_Points_of_Differentiable_Maps","16": "Sheaf_Theory","17": "Dynamical_Systems","18": "Low-Dimensional_Dynamical_Systems","19": "Hyperbolic_Dynamical_Systems","20": "Hamiltonian_Systems","21": "Bifurcation_of_Dynamical_Systems","22": "Manifold_Topology","23": "Index_Theory","24": "3-Dimensional_Manifolds","25": "4-Dimensional_Manifolds","26": "Geometric_Topology"},
                "X":{"1": "Analysis","2": "Continuous_Functions","3": "Inequalities","4": "Convex_Analysis","5": "Functions_of_Bounded_Variation","6": "Differential_Calculus","7": "Operational_Calculus","8": "Implicit_Function","9": "Elementary_Functions","10": "C∞_Functions,_Infinitesimal_Calculus","11": "Integration","12": "Line_and_Surface_Integrals","13": "Measure_Theory","14": "Integral_Calculus","15": "Invariant_Measures","16": "Length_and_Area","17": "Fractals","18": "Series","19": "Asymptotic_Series","20": "Polynomial_Approximation","21": "Orthogonal_Function_Systems","22": "Fourier_Series","23": "Fourier_Transform","24": "Wavelets","25": "Harmonic_Analysis,_Real_Analysis","26": "Quasiperiodic_Functions","27": "Laplace_Transform","28": "Integral_Transforms","29": "Potential_Theory","30": "Harmonic_Functions,Superharmonic_Functions","31": "Dirichlet_Problem","32": "Capacity","33": "Calculus_of_Variations","34": "Plateaus_Problem","35": "Isoperimetric_Problems"},
                "XI":{"1": "Complex_Analysis","2": "Holomorphic_Functions","3": "Power_Series","4": "Family_of_Holomorphic_Functions","5": "Maximum_Modulus_Principle","6": "Boundary_Behavior_of_Analytic_Functions","7": "Univalent_Functions","8": "Value_Distribution_Theory","9": "Complex_Approximation_Theory","10": "Riemann_Surfaces","11": "Analytic_Functions_on_Riemann_Surfaces","12": "Complex_Dynamical_Systems","13": "Conformal_Mapping","14": "Quasiconformal_Mapping","15": "Teichmüller_Space","16": "Kleinian_Group","17": "Multivariable_Analytic_Functions","18": "Analytic_Space","19": "¯∂_Equation","20": "Holomorphic_Mapping","21": "Plurisubharmonic_Functions","22": "CR_Manifold","23": "Kernel_Functions","24": "Siegel_Domain","25": "Periodic_Integration"},
                "XII":{"1": "Functional_Analysis","2": "Hilbert_Space","3": "Banach_Space","4": "Ordered_Linear_Space","5": "Linear_Topological_Space","6": "Function_Space","7": "Distributions","8": "Vector-Valued_Integration","9": "Linear_Operators","10": "Compact_Operators,_Nuclear_Operators","11": "Interpolation_Spaces","12": "Spectral_Analysis_of_Operators","13": "Operator_Inequalities","14": "Perturbation_of_Linear_Operators","15": "Operator_Semigroups,_Evolution_Equations","16": "Banach_Algebras","17": "C-Algebras","18": "Function_Algebras","19": "von_Neumann_Algebras","20": "Nonlinear_Functional_Analysis"},
                "XIII":{"1": "Differential_Equations","2": "Initial_Value_Problems_for_Ordinary_Differential_Equations","3": "Boundary_Value_Problems_for_Ordinary_Differential_Equations","4": "Linear_Ordinary_Differential_Equations","5": "Local_Theory_of_Linear_Ordinary_Differential_Equations","6": "Global_Theory_of_Linear_Ordinary_Differential_Equations","7": "Local_Theory_of_Nonlinear_Ordinary_Differential_Equations","8": "Global_Theory_of_Nonlinear_Ordinary_Differential_Equations","9": "Painlevé_Equations","10": "Nonlinear_Oscillations","11": "Nonlinear_Problems","12": "Stability","13": "Invariant_Integrals","14": "Difference_Equations","15": "Functional_Differential_Equations","16": "Total_Differential_Equations","17": "Solution_of_Partial_Differential_Equations","18": "Quasilinear_Equations,_Solvability","19": "Initial_Value_Problems_for_Partial_Differential_Equations","20": "Partial_Differential_Equations_in_Complex_Domains","21": "First-Order_Partial_Differential_Equations","22": "Monge-Ampère_Equations","23": "Elliptic_Partial_Differential_Equations","24": "Hyperbolic_Partial_Differential_Equations","25": "Parabolic_Partial_Differential_Equations","26": "Mixed_Type_Partial_Differential_Equations","27": "Inequalities_in_Differential_Equations","28": "Greens_Functions,_Greens_Operators","29": "Integral_Equations","30": "Integro-Differential_Equations","31": "Special_Function_Equations","32": "Microlocal_Analysis_and_Pseudodifferential_Operators"},
                "XIV":{"1": "Special_Functions","2": "Generating_Functions","3": "Elliptic_Functions","4": "Gamma_Function","5": "Hypergeometric_Functions","6": "Spherical_Harmonics","7": "Confluent_Hypergeometric_Functions","8": "Bessel_Functions","9": "Ellipsoidal_Harmonic_Functions","10": "Mathieu_Functions","11": "q-Series","12": "Polylogarithm_Functions","13": "Special_Orthogonal_Polynomials"},
                "XV":{"1": "Numerical_Analysis","2": "Numerical_Solutions_of_Linear_Systems","3": "Numerical_Solutions_of_Nonlinear_Equations","4": "Numerical_Eigenvalue_Computation","5": "Numerical_Integration_Methods","6": "Numerical_Solutions_of_Ordinary_Differential_Equations","7": "Numerical_Solutions_of_Partial_Differential_Equations","8": "Finite_Difference_Methods","9": "Finite_Element_Methods","10": "Function_Approximation_Methods","11": "Certified_Numerical_Computations"},
                "XVI":{"1": "Mathematical_Modeling","2": "Reaction-Diffusion_Equations","3": "Free_Boundary_Problems","4": "Variational_Analysis","5": "Fluid_Equations","6": "Conservation_Laws","7": "Nonlinear_Wave_and_Dispersion_Equations","8": "Scattering_Theory","9": "Inverse_Problems","10": "Viscous_Solutions"},
                "XVII":{"1": "Probability_Theory","2": "Probability_Measure","3": "Stochastic_Processes","4": "Limit_Theorems_in_Probability_Theory","5": "Markov_Processes","6": "Markov_Chains","7": "Brownian_Motion","8": "Lévy_Processes","9": "Martingales","10": "Diffusion_Processes","11": "Stochastic_Differential_Equations","12": "Martingale_Analysis","13": "Measure-Valued_Stochastic_Processes","14": "Gaussian_Processes","15": "Stationary_Processes","16": "Ergodic_Theory","17": "Probability_Control_and_Filtering","18": "Probabilistic_Methods_in_Statistical_Physics"},
                "XVIII":{"1": "Statistics","2": "Statistical_Models_and_Inference","3": "Statistical_Quantities_and_Sample_Distributions","4": "Statistical_Estimation","5": "Statistical_Hypothesis_Testing","6": "Multivariate_Analysis","7": "Robust_Nonparametric_Methods","8": "Experimental_Design","9": "Sampling_Methods","10": "Actuarial_Mathematics","11": "Time_Series_Analysis","12": "Inference_for_Stochastic_Processes","13": "Statistical_Computing","14": "Information_Geometry"},
                "XIX":{"1": "Discrete_Mathematics_and_Combinatorics","2": "Graph_Theory","3": "Enumerative_Combinatorics","4": "Matroids","5": "Design_Theory","6": "Discrete_Geometry","7": "Extremal_Set_Theory","8": "Algebraic_Combinatorics"},
                "XX":{"1": "Mathematics_in_Computer_Science","2": "Formal_Language_Theory_and_Automata","3": "Computational_Complexity_Theory","4": "Information_Theory","5": "Coding_Theory","6": "Cryptography","7": "Computer_Algebra","8": "Computational_Geometry","9": "Randomness_and_Monte_Carlo_Methods"},
                "XXI":{"1": "Mathematical_Programming","2": "Linear_Programming","3": "Nonlinear_Programming","4": "Semidefinite_Programming","5": "Global_Optimization","6": "Network_Flow","7": "Discrete_Convex_Analysis","8": "Integer_Programming","9": "Combinatorial_Optimization","10": "Dynamic_Programming","11": "Stochastic_Programming","12": "Game_Theory","13": "Complementarity_Problem","14": "Control_Theory","15": "Operations_Research","16": "Portfolio_Theory","17": "Markov_Decision_Process"},
                "XXII":{"1": "Units_and_Dimensions","2": "Dimensional_Analysis","3": "Variational_Principles_in_Physics","4": "Classical_Mechanics","5": "Celestial_Mechanics","6": "Astrophysics","7": "Three-Body_Problem","8": "Fluid_Mechanics","9": "Plasma_Physics","10": "Turbulence","11": "Complex_Systems","12": "Phase_Transitions","13": "Oscillations_and_Waves","14": "Geometrical_Optics","15": "Electromagnetism","16": "Circuits","17": "Thermodynamics","18": "Statistical_Mechanics","19": "Theory_of_Relativity","20": "Unified_Field_Theories","21": "Quantum_Mechanics","22": "Lorentz_Group","23": "Lie_Algebras","24": "Second_Quantization","25": "Field_Theory","26": "S-Matrix","27": "Feynman_Integrals","28": "Particle_Physics","29": "Renormalization_Group","30": "Integrable_Models","31": "Solitons","32": "Conformal_Field_Theory","33": "Approximation_Methods_in_Physics"},
                "XXIII":{"1": "Egyptian_and_Babylonian_Mathematics","2": "Greek_and_Roman_Mathematics","3": "Mathematics_in_Medieval_Europe","4": "Arabic_Mathematics","5": "Indian_Mathematics","6": "Chinese_Mathematics","7": "Japanese_Mathematics","8": "Mathematics_in_the_Renaissance","9": "Mathematics_in_the_17th_Century","10": "Mathematics_in_the_18th_Century","11": "Mathematics_in_the_19th_Century"}}

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
                        obj["data"]["parent"] = "/"+parent[1]+"/"
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
                    obj["data"]["id"] = "/"+id[1]+"/"
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
                        obj["data"]["parent"] = "/"+parent[1]+"/"
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
                    obj["data"]["id"] = "/"+id[1]+"/"
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