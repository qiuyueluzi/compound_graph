
/*
createGraph.pyで出力されたファイルとcytoscape.jsを使って
グラフの描画を行う
*/
$(function(){
    $.when($.getJSON('./graph_attrs/graph_Hierar_replace.json')).then((dot_graph) => {
        $(".has-sub").children(".sub").stop().slideToggle();
        // cytoscapeグラフの作成(初期化)
        let cy = window.cy = cytoscape({
            container: document.getElementById('graph'),
            elements: [],
            boxSelectionEnabled: true,
            autounselectify: false,
            selectionType: "additive",
            wheelSensitivity: 0.1,
            autounselectify: true,
            zoom: 0.025,
            
        });
        
        cy.add(dot_graph["parents"]); //先にparentsを描画しなければ正しくレイアウトされないため、parentsから描画する
        cy.add(dot_graph["eleObjs"]);
        const nodeData = (dot_graph["eleObjs"]);
        
        let directories = dot_graph["parents"].map(parent => parent.data["id"]); //ディレクトリ一覧を作成
        
        const id2relatedElements = new Map(); //全ノードのid・親子(複合)・接続エッジなどを格納
        /**id       :ノードのid
         * children :ノードのクラスタリング上の子ノード情報
         * edges    :ノード，子ノードと接続している全てのエッジ情報
         * parent   :ノードのクラスタリング上の親ノード情報
         * ancestors:ノードの親ノードを含む祖先ノード情報
         * isParent :ノードが子ノードを持つかどうか
         * removed  :ノードが非表示となっているかどうか
         * 
         * Conpound graphsを使用しているとcytoscapeのノード非表示関数ele.hidden()が機能しなかったため、当コードでは削除/復元によって代用している。
         * id2relatedElementsは復元時のデータ読み込みに使用
         * 
        */
        let nodes = cy.nodes();
        nodes.forEach(node => { //初期状態での全ノードの、関連するエッジの情報を記録
            let currentNode = cy.$(node);
            let id = currentNode.data('id');
            
            let childrenNodes = currentNode.children();
            let connectedEdges = currentNode.connectedEdges();
            let childConnectedEdges = currentNode.descendants().connectedEdges();
            let parentNode = currentNode.data('parent');
            let ancestorNodes = currentNode.ancestors().map(ancestor => ancestor.id());
            ancestorNodes.sort().reverse();
            
            let isParent = childrenNodes.length > 0;
            currentNode.style({
                'shape': isParent ? 'square' : 'ellipse',
                'width': isParent ? '200' : '80',
                'height': isParent ? '200' : '80',
                'color': '#000000',
                'text-outline-color': '#FFFFFF',
                'text-valign': isParent ? 'top' : 'center',
            });
            
            
            id2relatedElements.set(id, {
                children :childrenNodes, 
                edges: connectedEdges.union(childConnectedEdges), 
                parent: parentNode, 
                ancestors: ancestorNodes, 
                isParent: isParent, 
                removed: false
            });
        })
        
        let layout = cy.elements().layout({ //klayレイアウトを適用
            name: "klay",
            spacingFactor: 10
        })
        //layout.run()
        
        let contextMenu = cy.contextMenus({ //右クリック時のコンテキストメニュー
            evtType: ['cxttap'],
            menuItems: [
                {
                    id: 'Highlight Connected Nodes',
                    content: 'Highlight Connected Nodes',
                    tooltipText: 'Highlight Connected Nodes',
                    selector: 'node',
                    onClickFunction: (event) => {
                        event.target.trigger("clickElement", event);
                    },
                    hasTrailingDivider: true,
                },
                {
                    id: 'Go to Source Code',
                    content: 'Go to Source Code',
                    tooltipText: 'Go to Source Code',
                    selector: 'node',
                    hasTrailingDivider: true,
                    onClickFunction: (event) => {
                        try {  // your browser may block popups
                            window.open(event.target.data("href"));
                        } catch(e){  // fall back on url change
                            window.location.href = event.data("href");
                        }
                    },
                },
                {
                    id: 'open/close',
                    content: 'open/close',
                    tooltipText: 'open/close',
                    selector: 'node',
                    hasTrailingDivider: true,
                    onClickFunction: (event) => {
                        event.target.trigger("doubleTap", event);
                    }
                },
                {
                    id: "Highlight Same Cluster Nodes",
                    content: "Highlight Same Cluster Nodes",
                    tooltipText: "Highlight Same Cluster Nodes",
                    selector: 'node',
                    onClickFunction: (event) => {
                        event.target.trigger("coloring", event);
                    },
                    hasTrailingDivider: true,
                }
            ],
        });

        
        // Set graph style
        cy.style([
            /* 初期状態のスタイル */
            {
                selector: "node",
                css: {"background-color": "#000000", "shape": "ellipse", "width": "80", "height": "80",
                "content": "data(name)", 'font-size': 60, "opacity": 1, "z-index": 1,
                "text-halign":"right", "text-valign": "center", "font-style": "normal",
                "font-weight": "bold", "color": "#000000",
                "text-outline-color": "#FFFFFF", "text-outline-opacity": 1, "text-outline-width": 6}
            },
            {
                selector: 'node:parent',
                css: {
                    'content': 'data(name)',
                    'font-size': 0,
                    "text-outline-color": '#FFFFFF',
                    'color': '#000000',
                    'text-valign': 'top',
                    'text-halign': 'center',
                    'background-color': '#20bd3d',
                    'background-opacity': 0
                }
            },
            {
                selector: "edge",
                css: {"line-color": "black", "target-arrow-shape": "triangle", "curve-style": "straight",
                "target-arrow-color": "black", "arrow-scale": 3, "width": 5, "opacity": 0.3, "z-index": 1,}
            },
            /* ノードが左クリックされたときに適応されるスタイル */
            // 選択されたノード全てのスタイル
            {
                selector: "node.highlight",
                css: {'font-size': 120,  "width": 250, "height": 250, "font-size": 100,
                "content": "data(name)", "opacity": 1, "z-index": 10}
            },
            // 選択(左クリック)されたノードのスタイル
            {
                selector: "node.selected",
                css: {"background-color": "#99ff00", "color": "#006633", "width": 300, "height": 300,
                "text-outline-color": "#99ff00", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            // 選択された(強調表示する)祖先のスタイル
            {
                selector: "node.selected_ancestors0", 
                css: {"background-color": "#ffbb00", "color": "#660033",
                "text-outline-color": "#ffbb00", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors1",
                css: {"background-color": "#ff9900", "color": "#660033",
                "text-outline-color": "#ff9900", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors2",
                css: {"background-color": "#ff7700", "color": "#660033",
                "text-outline-color": "#ff7700", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors3",
                css: {"background-color": "#ff4400",  "color": "#660033",    
                "text-outline-color": "#ff4400", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors4",
                css: {"background-color": "#ff0000",  "color": "#660033",
                "text-outline-color": "#ff0000", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            // 選択された(強調表示する)子孫のスタイル
            {
                selector: "node.selected_descendants0",
                css: {"background-color": "#00ffff", "color": "#330066",
                "text-outline-color": "#00ffff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants1",
                css: {"background-color": "#00ddff", "color": "#330066",
                "text-outline-color": "#00ddff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants2",
                css: {"background-color": "#00bbff", "color": "#330066",
                "text-outline-color": "#00bbff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants3",
                css: {"background-color": "#0077ff", "color": "#330066",
                "text-outline-color": "#0077ff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants4",
                css: {"background-color": "#0000ff", "color": "#330066",
                "text-outline-color": "#0000ff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.interaction",
                css: {"background-color": "#ff00ff", "color": "#330066",
                "text-outline-color": "#ff00ff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            // 強調表示されたノードをつなぐエッジのスタイル
            {
                selector: "edge.highlight",
                css: {"line-color": "#004400", "curve-style": "straight",
                "target-arrow-color": "#004400", "arrow-scale": 5, "width": 10, "opacity": 1, "z-index": 20}
            },
            /* ダミーノードを指すエッジが選択された場合 */
            {
                selector: cy.nodes().edgesTo("node.selected[?is_dummy]"),
                css: {"line-color": "green", "target-arrow-shape": "none", "curve-style": "straight",
                "arrow-scale": 10, "width": 5, "z-index": 10, width: 20}
            },
            // 選択されていないノードの色を変更
            {
                selector: "node.faded",
                css: {"background-color": "#808080", "text-outline-color": "#808080", "color": "#ffffff"}
            },
            // 選択されていないノードとエッジは薄く表示する
            {
                selector: ".faded",
                css: {"opacity": 0.15, "z-index": 0}
            },
            {
                selector: "node:parent.faded",
                css: {"opacity": 1}
            },
            {
                selector: "node.select",
                css: {"background-color": "#FF0000"}
            },
            {
                selector: "node.cluster_indigo",
                css: {"width": 100, "height": 100, "font-size": 80,
                "content": "data(name)", "opacity": 1, "z-index": 10, "background-color": "#332288"}
            },
            {
                selector: "node.cluster_cyan",
                css: {"width": 100, "height": 100, "font-size": 80,
                "content": "data(name)", "opacity": 1, "z-index": 10, "background-color": "#88CCEE"}
            },
            {
                selector: "node.cluster_teal",
                css: {"width": 100, "height": 100, "font-size": 80,
                "content": "data(name)", "opacity": 1, "z-index": 10, "background-color": "#44AA99"}
            },
            {
                selector: "node.cluster_green",
                css: {"width": 100, "height": 100, "font-size": 80,
                "content": "data(name)", "opacity": 1, "z-index": 10, "background-color": "#117733"}
            },
            {
                selector: "node.cluster_olive",
                css: {"width": 100, "height": 100, "font-size": 80,
                "content": "data(name)", "opacity": 1, "z-index": 10, "background-color": "#999933"}
            },
            {
                selector: "node.cluster_sand",
                css: {"width": 100, "height": 100, "font-size": 80,
                "content": "data(name)", "opacity": 1, "z-index": 10, "background-color": "#DDCC77"}
            },
            {
                selector: "node.cluster_rose",
                css: {"width": 100, "height": 100, "font-size": 80,
                "content": "data(name)", "opacity": 1, "z-index": 10, "background-color": "#CC6677"}
            },
            {
                selector: "node.cluster_wine",
                css: {"width": 100, "height": 100, "font-size": 80,
                "content": "data(name)", "opacity": 1, "z-index": 10, "background-color": "#882255"}
            },
            {
                
                selector: "node.cluster_purple",
                css: {"width": 100, "height": 100, "font-size": 80,
                "content": "data(name)", "opacity": 1, "z-index": 10, "background-color": "#AA4499"}
            },
            
        ]);
        
    /* 初期状態の設定 */
        
    all_nodes_positions = cy.nodes().positions();  //ノードの位置を記録　今のところ使ってない
    cy.fit(cy.nodes().orphans());
    let allAncestors = nodes.ancestors();
    let allOrphans = nodes.orphans();
    let common = allAncestors&&allOrphans;
    for(let i=common.length-1; i>=0; i--){//TARSKIを配列から削除
        if(!common[i]._private.data.id.match(/^[\/]/)){
            common.splice(i, 1);
        }
    }
    cy.style().selector(common).style({
        'content': 'data(name)',
        'font-size': 500,
        "text-outline-color": '#FFFFFF',
        'color': '#000000',
        'text-valign': 'top',
        'text-halign': 'center',
        'background-color': '#20bd3d',
        'background-opacity': 0.25
    })  
    .update()
    let cluster = [];
    $("#open").prop("disabled", true);
    let parent_nodes_positions = new Map();
    (allAncestors&&allOrphans).forEach(parent => {
        let position = parent.position();
        parent_nodes_positions.set(parent._private.data.id, {x:position.x, y:position.y});
    })
    
    // 強調表示する祖先、子孫の世代数の初期化
    let ancestor_generations = 1;
    let descendant_generations = 1;
    
    /* 検索機能の追加 */
    // 全ノード名の取得
    let all_article_names = [];
    let all_parent_names = [];
    nodes.orphans().forEach(function(parent){
        if(parent.isParent())all_parent_names.push([parent.data("name"), "/"+parent.data("name")]);
        function childrenPush(parent, parentFullname){
            parent.children().forEach(function(child){
                if(child.isParent())all_parent_names.push([child.data("name"), parentFullname+"/"+child.data("name")]);
                if(child.children())childrenPush(child, parentFullname+"/"+child.data("name"));
            })
        }
        childrenPush(parent, "/"+parent.data("name"))

        all_parent_names.push("")
    })
    cy.nodes("[!is_dummy]").forEach(function(node){
        if(!id2relatedElements.get(node.id()).isParent) all_article_names.push(node.data("name"));
        //else all_parent_names.push(node.data("name"));
    });
    all_article_names.sort();

    // 検索時のサジェスト・ディレクトリ一覧表示に使用するdatalistに全ノード名を追加
    for (let article_name of all_article_names){
        $("#article_list").append($("<option/>").val(article_name).html(article_name));
    }
    let generation1, generation2, generation3;
    
    /*for (let parent_name of all_parent_names.sort().reverse()){
        if(parent_name){
            let parentsDisplayName = parent_name[0];
            let parentsFullName = parent_name[1];
            switch ((parentsFullName.match( /\//g)||[]).length) {
                case 1:
                    cluster.push("\r\n")//?
                    $("#parent_list").prepend("<details id="+parentsFullName+" class=sideMenu><summary>"+parentsDisplayName+"</summary></details>")
                    generation1 = "#\\" + parentsFullName;
                    if(id2relatedElements.get(parentsFullName).isParent){
                        for(let child of id2relatedElements.get(parentsFullName).children){
                            if(!id2relatedElements.get(child._private.data.id).isParent){
                                $(generation1).append("<li id="+child._private.data.id+">"+child._private.data.id+"</li>");
                                //$(generation1).append("<li id="+child._private.data.id+"><input type=\"checkbox\">"+child._private.data.id+"</li>");
                                cluster.push(child._private.data.id+"\r\n");
                            }
                        }
                    }
                    //$(generation1).append("<input type=\"button\" class=\"btn btn-primary btn-sm btnGen1\" value=\"sea\" id="+generation1+" >");
                    break;
                      
                case 2:
                    $(generation1).prepend("<details id="+parentsFullName+" class=\"indent1 sideMenu\"><summary>"+parentsDisplayName+"</summary></details>")
                    let indexOfSlash = parentsFullName.lastIndexOf("/")
                    generation2 = "#\\" + parentsFullName.slice(0, indexOfSlash) + "\\" + parentsFullName.slice(indexOfSlash)
                    if(id2relatedElements.get(parentsFullName).isParent){
                        for(let child of id2relatedElements.get(parentsFullName).children){
                            if(!id2relatedElements.get(child._private.data.id).isParent){
                                $(generation2).append("<li id="+child._private.data.id+">"+child._private.data.id+"</li>")
                                //$(generation2).append("<li id="+child._private.data.id+"><input type=\"checkbox\">"+child._private.data.id+"</li>")
                                cluster.push(child._private.data.id+"\r\n");
                            }
                        }
                    }
                    $(generation2).append("<li class=\"btnGen1\" id="+generation2+">highlight</li>");
                    break;
                    
                case 3:
                    $(generation2).prepend("<details id="+parentsFullName+" class=\"indent2 sideMenu\"><summary>"+parentsDisplayName+"</summary></details>")
                    let indexOfSlash2 = parentsFullName.indexOf("/",1)
                    let indexOfSlash3 = parentsFullName.lastIndexOf("/")
                    generation3 = "#\\" + parentsFullName.slice(0, indexOfSlash2) + "\\" + parentsFullName.slice(indexOfSlash2, indexOfSlash3) + "\\" + parentsFullName.slice(indexOfSlash3)
                    if(id2relatedElements.get(parentsFullName).isParent){
                        for(let child of id2relatedElements.get(parentsFullName).children){
                            if(!id2relatedElements.get(child._private.data.id).isParent){
                                $(generation3).append("<li id="+child._private.data.id+">"+child._private.data.id+"</li>")
                                //$(generation3).append("<li id="+child._private.data.id+"><input type=\"checkbox\">"+child._private.data.id+"</li>")
                                cluster.push(child._private.data.id+"\r\n");
                            }
                        }
                    }
                    $(generation3).append("<li class=\"btnGen1\" id="+generation3+">highlight</li>");
                    break;
                default:
                    break;
            }

        }
        else {
            generation1="";
            generation2="";
            generation3="";
        }
    }*/
    let level1 = {1: "Math_Logic", 2: "Sets_and_Topology", 3: "Algebra", 4: "Number_Theory", 5: "Groups_and_Rep",
    6: "Alg_Geometry", 7: "Geometry", 8: "Diff_Geometry", 9: "Topology", 10: "Analysis",
    11: "Complex_An", 12: "Func_An", 13: "Diff_Eqns", 14: "Spec_Func", 15: "Num_An",
    16: "Appl_An", 17: "Prob_Theory", 18: "Stats", 19: "Disc_Math", 
    20: "Info_Math", 21: "Opt_Theory", 22: "Mech_Phys", 23: "Hist_Math"}
    let level2 = {1:{"1": "Foundations of Mathematics","2": "Semantics of Formal Systems","3": "Formal Systems and Proofs","4": "Computable Functions","5": "Model Theory","6": "Stability Theory","7": "Nonstandard Analysis","8": "Theory of Ordinal Numbers","9": "Axiomatic Set Theory","10": "Forcing","11": "Large Cardinals","12": "Descriptive Set Theory","13": "Recursive Theory","14": "Decision Problems","15": "Theory of Degrees","16": "Constructive Ordinals","17": "Proof Theory","18": "Gödel's Incompleteness Theorems","19": "Nonstandard Models of Arithmetic","20": "Type Theory and Lambda Calculus","21": "Herbrand's Theorem and Deduction Principles","22": "Nonstandard Logic","23": "Reverse Mathematics"},
    2:{"1": "Sets","2": "Relations","3": "Equivalence Relations","4": "Functions","5": "Axiom of Choice","6": "Cardinality","7": "Structures","8": "Permutations and Combinations","9": "Numbers","10": "Real Numbers and the Real Line","11": "Complex Numbers and the Complex Plane","12": "Order","13": "Ordinal Numbers","14": "Lattices","15": "Boolean Algebra","16": "Topological Spaces","17": "Metric Spaces","18": "Plane Regions","19": "Convergence","20": "Connectedness","21": "Dimension","22": "Uniform Spaces","23": "Uniform Convergence","24": "Categories and Functors","25": "Inductive and Projective Limits","26": "Sheaves"},
    3:{"1": "Algebra","2": "Matrices","3": "Determinants","4": "Polynomials","5": "Algebraic Equations","6": "Fields","7": "Galois Theory","8": "Vector Spaces","9": "Tensor and Exterior Products","10": "Rings","11": "Multivariate Rings","12": "Modules","13": "Representations of Multivariate Rings","14": "Homological Algebra","15": "Hopf Algebras","16": "Commutative Rings","17": "Noetherian Rings","18": "Polynomial Rings","19": "Invariants","20": "Power Series Rings","21": "Prime Ideals and Factorization Rings","22": "Homological Algebra of Commutative Rings","23": "Excellent Rings","24": "Hensel Rings and Approximation Theorems","25": "Adherent Closure of Ideals","26": "Quadratic Forms","27": "Clifford Algebras","28": "Differential Rings","29": "Witt Vectors","30": "Valuations","31": "Adèles and Ideals","32": "Cayley Algebras","33": "Jordan Algebras"},
    4:{"1": "Number Theory","2": "Elementary Number Theory","3": "Continued Fractions","4": "Number-Theoretic Functions","5": "Additive Number Theory","6": "Distribution of Prime Numbers","7": "Geometry of Numbers and Approximations in Number Theory","8": "Transcendental Numbers","9": "Diophantine Equations","10": "Quadratic Number Fields","11": "Algebraic Number Theory","12": "Local Fields","13": "Class Field Theory","14": "Iwasawa Theory","15": "Algebraic K-Theory","16": "Arithmetic Geometry","17": "Fermat's Last Theorem","18": "Algebraic Groups over Number Fields","19": "Modular Forms","20": "Shimura Varieties","21": "Dirichlet Series","22": "Zeta Functions","23": "Pseudo-Homogeneous Vector Spaces"},
    5:{"1": "Group","2": "Abelian Group","3": "Finite Group","4": "Finite Simple Group","5": "Crystallographic Group","6": "Classical Group","7": "Topological Group","8": "Compact Group","9": "Lie Group","10": "Lie Algebra","11": "Algebraic Group","12": "Symmetric Space","13": "Group Actions on Homogeneous Spaces","14": "Discrete Group","15": "Representation Theory","16": "Modular Representation","17": "Unitary Representation","18": "Infinite-Dimensional Representation","19": "Group Actions and Invariants","20": "D-module","21": "Quantum Group","22": "Infinite-Dimensional Lie Algebra"},
    6:{"1": "Algebraic Geometry","2": "Algebraic Curves","3": "Algebraic Surfaces, Complex Analytic Surfaces","4": "Algebraic Varieties A: Sheaves and Cohomology","5": "Algebraic Varieties B: Sheaves and Cohomology","6": "Algebraic Varieties C: Rational Maps and Resolution of Singularities","7": "Algebraic Varieties D: Fibrations and Abelian Varieties","8": "Algebraic Varieties E: Riemann-Roch and Chow Rings","9": "Algebraic Varieties F: Algebraic Spaces and Formal Schemes","10": "Algebraic Varieties G: Polarized Varieties","11": "Algebraic Varieties H: Topology and Comparison Theorems","12": "Algebraic Vector Bundles","13": "Hodge Theory","14": "Abelian Varieties","15": "Rational and Fan0 Varieties","16": "Birational Geometry","17": "Toric Varieties","18": "Intersection Theory","19": "Singularity Theory","20": "Moduli Problems"},
    7:{"1": "Geometry","2": "Euclidean Geometry","3": "Euclidean Space","4": "Non-Euclidean Geometry","5": "Projective Geometry","6": "Affine Geometry","7": "Conformal Geometry","8": "Erlangen Program","9": "Foundations of Geometry","10": "Construction Problems","11": "Regular Polyhedra","12": "Pi (π)","13": "Trigonometry","14": "Quadratic Curves and Surfaces","15": "Convex Sets","16": "Coordinates","17": "Vector Analysis","18": "Curves","19": "Surfaces","20": "Four-Color Problem","21": "Combinatorial Geometry"},
    8:{"1": "Differential Geometry","2": "Manifold","3": "Riemannian Manifold","4": "Connection","5": "Tensor and Spinor","6": "Global Riemannian Geometry","7": "Differential Geometry of Homogeneous Spaces","8": "G-Structures and Equivalence Problems","9": "Complex Manifold","10": "Harmonic Analysis","11": "Differential Geometry of Curves and Surfaces","12": "Differential Geometry of Submanifolds","13": "Minimal Submanifolds","14": "Geometric Measure Theory","15": "Harmonic Maps","16": "Morse Theory","17": "Affine Differential Geometry","18": "Finsler Space","19": "Integral Geometry","20": "Spectral Geometry","21": "Rigidity and Geometric Group Theory","22": "Symplectic and Contact Geometry","23": "Moduli Spaces and Partial Differential Equations","24": "Special Geometry"},
    9:{"1": "Topology","2": "Fundamental Group","3": "Covering Spaces","4": "Degree of a Mapping","5": "Complex","6": "Homology Theory","7": "Fixed Point Theorem","8": "Homotopy Theory","9": "Fiber Bundle","10": "Cobordism Theory","11": "Characteristic Classes","12": "K-Theory","13": "Knot Theory","14": "Transformation Group","15": "Singular Points of Differentiable Maps","16": "Sheaf Theory","17": "Dynamical Systems","18": "Low-Dimensional Dynamical Systems","19": "Hyperbolic Dynamical Systems","20": "Hamiltonian Systems","21": "Bifurcation of Dynamical Systems","22": "Manifold Topology","23": "Index Theory","24": "3-Dimensional Manifolds","25": "4-Dimensional Manifolds","26": "Geometric Topology"},
    10:{"1": "Analysis","2": "Continuous Functions","3": "Inequalities","4": "Convex Analysis","5": "Functions of Bounded Variation","6": "Differential Calculus","7": "Operational Calculus","8": "Implicit Function","9": "Elementary Functions","10": "C∞ Functions, Infinitesimal Calculus","11": "Integration","12": "Line and Surface Integrals","13": "Measure Theory","14": "Integral Calculus","15": "Invariant Measures","16": "Length and Area","17": "Fractals","18": "Series","19": "Asymptotic Series","20": "Polynomial Approximation","21": "Orthogonal Function Systems","22": "Fourier Series","23": "Fourier Transform","24": "Wavelets","25": "Harmonic Analysis, Real Analysis","26": "Quasiperiodic Functions","27": "Laplace Transform","28": "Integral Transforms","29": "Potential Theory","30": "Harmonic Functions, Superharmonic Functions","31": "Dirichlet Problem","32": "Capacity","33": "Calculus of Variations","34": "Plateau's Problem","35": "Isoperimetric Problems"},
    11:{"1": "Complex Analysis","2": "Holomorphic Functions","3": "Power Series","4": "Family of Holomorphic Functions","5": "Maximum Modulus Principle","6": "Boundary Behavior of Analytic Functions","7": "Univalent Functions","8": "Value Distribution Theory","9": "Complex Approximation Theory","10": "Riemann Surfaces","11": "Analytic Functions on Riemann Surfaces","12": "Complex Dynamical Systems","13": "Conformal Mapping","14": "Quasiconformal Mapping","15": "Teichmüller Space","16": "Kleinian Group","17": "Multivariable Analytic Functions","18": "Analytic Space","19": "¯∂ Equation","20": "Holomorphic Mapping","21": "Plurisubharmonic Functions","22": "CR Manifold","23": "Kernel Functions","24": "Siegel Domain","25": "Periodic Integration"},
    12:{"1": "Functional Analysis","2": "Hilbert Space","3": "Banach Space","4": "Ordered Linear Space","5": "Linear Topological Space","6": "Function Space","7": "Distributions (Generalized Functions)","8": "Vector-Valued Integration","9": "Linear Operators","10": "Compact Operators, Nuclear Operators","11": "Interpolation Spaces","12": "Spectral Analysis of Operators","13": "Operator Inequalities","14": "Perturbation of Linear Operators","15": "Operator Semigroups, Evolution Equations","16": "Banach Algebras","17": "C*-Algebras","18": "Function Algebras","19": "von Neumann Algebras","20": "Nonlinear Functional Analysis"},
    13:{"1": "Differential Equations","2": "Initial Value Problems for Ordinary Differential Equations","3": "Boundary Value Problems for Ordinary Differential Equations","4": "Linear Ordinary Differential Equations","5": "Local Theory of Linear Ordinary Differential Equations","6": "Global Theory of Linear Ordinary Differential Equations","7": "Local Theory of Nonlinear Ordinary Differential Equations","8": "Global Theory of Nonlinear Ordinary Differential Equations","9": "Painlevé Equations","10": "Nonlinear Oscillations","11": "Nonlinear Problems","12": "Stability","13": "Invariant Integrals","14": "Difference Equations","15": "Functional Differential Equations","16": "Total Differential Equations","17": "Solution of Partial Differential Equations","18": "Quasilinear Equations, Solvability","19": "Initial Value Problems for Partial Differential Equations","20": "Partial Differential Equations in Complex Domains","21": "First-Order Partial Differential Equations","22": "Monge-Ampère Equations","23": "Elliptic Partial Differential Equations","24": "Hyperbolic Partial Differential Equations","25": "Parabolic Partial Differential Equations","26": "Mixed Type Partial Differential Equations","27": "Inequalities in Differential Equations","28": "Green's Functions, Green's Operators","29": "Integral Equations","30": "Integro-Differential Equations","31": "Special Function Equations","32": "Microlocal Analysis and Pseudodifferential Operators"},
    14:{"1": "Special Functions","2": "Generating Functions","3": "Elliptic Functions","4": "Gamma Function","5": "Hypergeometric Functions","6": "Spherical Harmonics","7": "Confluent Hypergeometric Functions","8": "Bessel Functions","9": "Ellipsoidal Harmonic Functions","10": "Mathieu Functions","11": "q-Series","12": "Polylogarithm Functions","13": "Special Orthogonal Polynomials"},
    15:{"1": "Numerical Analysis","2": "Numerical Solutions of Linear Systems","3": "Numerical Solutions of Nonlinear Equations","4": "Numerical Eigenvalue Computation","5": "Numerical Integration Methods","6": "Numerical Solutions of Ordinary Differential Equations","7": "Numerical Solutions of Partial Differential Equations","8": "Finite Difference Methods","9": "Finite Element Methods","10": "Function Approximation Methods","11": "Certified Numerical Computations"},
    16:{"1": "Mathematical Modeling","2": "Reaction-Diffusion Equations","3": "Free Boundary Problems","4": "Variational Analysis","5": "Fluid Equations","6": "Conservation Laws","7": "Nonlinear Wave and Dispersion Equations","8": "Scattering Theory","9": "Inverse Problems","10": "Viscous Solutions"},
    17:{"1": "Probability Theory","2": "Probability Measure","3": "Stochastic Processes","4": "Limit Theorems in Probability Theory","5": "Markov Processes","6": "Markov Chains","7": "Brownian Motion","8": "Lévy Processes","9": "Martingales","10": "Diffusion Processes","11": "Stochastic Differential Equations","12": "Martingale Analysis","13": "Measure-Valued Stochastic Processes","14": "Gaussian Processes","15": "Stationary Processes","16": "Ergodic Theory","17": "Probability Control and Filtering","18": "Probabilistic Methods in Statistical Physics"},
    18:{"1": "Statistics","2": "Statistical Models and Inference","3": "Statistical Quantities and Sample Distributions","4": "Statistical Estimation","5": "Statistical Hypothesis Testing","6": "Multivariate Analysis","7": "Robust Nonparametric Methods","8": "Experimental Design","9": "Sampling Methods","10": "Actuarial Mathematics","11": "Time Series Analysis","12": "Inference for Stochastic Processes","13": "Statistical Computing","14": "Information Geometry"},
    19:{"1": "Discrete Mathematics and Combinatorics","2": "Graph Theory","3": "Enumerative Combinatorics","4": "Matroids","5": "Design Theory","6": "Discrete Geometry","7": "Extremal Set Theory","8": "Algebraic Combinatorics"},
    20:{"1": "Mathematics in Computer Science","2": "Formal Language Theory and Automata","3": "Computational Complexity Theory","4": "Information Theory","5": "Coding Theory","6": "Cryptography","7": "Computer Algebra","8": "Computational Geometry","9": "Randomness and Monte Carlo Methods"},
    21:{"1": "Mathematical Programming","2": "Linear Programming","3": "Nonlinear Programming","4": "Semidefinite Programming","5": "Global Optimization","6": "Network Flow","7": "Discrete Convex Analysis","8": "Integer Programming","9": "Combinatorial Optimization","10": "Dynamic Programming","11": "Stochastic Programming","12": "Game Theory","13": "Complementarity Problem","14": "Control Theory","15": "Operations Research","16": "Portfolio Theory","17": "Markov Decision Process"},
    22:{"1": "Units and Dimensions","2": "Dimensional Analysis","3": "Variational Principles in Physics","4": "Classical Mechanics","5": "Celestial Mechanics","6": "Astrophysics","7": "Three-Body Problem","8": "Fluid Mechanics","9": "Plasma Physics","10": "Turbulence","11": "Complex Systems","12": "Phase Transitions","13": "Oscillations and Waves","14": "Geometrical Optics","15": "Electromagnetism","16": "Circuits","17": "Thermodynamics","18": "Statistical Mechanics","19": "Theory of Relativity","20": "Unified Field Theories","21": "Quantum Mechanics","22": "Lorentz Group","23": "Lie Algebras","24": "Second Quantization","25": "Field Theory","26": "S-Matrix","27": "Feynman Integrals","28": "Particle Physics","29": "Renormalization Group","30": "Integrable Models","31": "Solitons","32": "Conformal Field Theory","33": "Approximation Methods in Physics"},
    23:{"1": "Egyptian and Babylonian Mathematics","2": "Greek and Roman Mathematics","3": "Mathematics in Medieval Europe","4": "Arabic Mathematics","5": "Indian Mathematics","6": "Chinese Mathematics","7": "Japanese Mathematics (Wagaku)","8": "Mathematics in the Renaissance","9": "Mathematics in the 17th Century","10": "Mathematics in the 18th Century","11": "Mathematics in the 19th Century"}}

    createAccordionMenu(level1, level2);

    // グループ化されたノードの親ノードを取得します

    
    // 同じ親を持つノードをフィルタリングします
    up = 0;
    edgecount = 0;
    cy.edges().forEach(edge => {
        var sourceNode = edge.source();  // エッジの始点を取得
        var targetNode = edge.target();  // エッジの終点を取得
        if (sourceNode.position('y') > targetNode.position('y')){
            up++;
            edgecount++;
        }
        else{
            edgecount++;
        }
    });
    console.log(up/edgecount)
    

    let all_cluster_color = ["cluster_indigo", "cluster_cyan", "cluster_teal", "cluster_green", "cluster_olive", "cluster_sand", "cluster_rose", "cluster_wine", "cluster_purple"];
    let color_number = 0;
    $("li").click(function(){
        if($(this).hasClass("btnGen1")){
            let cluster = cy.$(this.id).descendants();
            console.log(cluster,this,this.id)
            cluster.forEach(child => {
                if(!child.isParent()){
                    child.addClass(all_cluster_color[color_number]);
                    let element = document.getElementById(child._private.data.id);
                    element.style.color = "#332288";
                }
            });
            document.getElementById(all_cluster_color[color_number]).innerHTML = cy.$(this.id).id()
            color_number++;
            if(color_number >= all_cluster_color.length)color_number = 0;
        }
        else{
            let nodeID = $(this).attr("id")
            searchNode(nodeID, nodes, id2relatedElements)
        }
    });

    // searchボタンをクリックしたら検索開始
    $("#search").click(function() {
        searchNode($("#article_name").val(), nodes, id2relatedElements)
    });
    // 入力が終わった時も検索を開始する
    $("#article_name").change(function() {
        searchNode($("#article_name").val(), nodes, id2relatedElements)
    });

    function searchNode(nodeName, nodes, id2relatedElements){
                // dropdownで選択したノード名、または記述したノード名を取得
                let select_node_name = nodeName;
                let select_node = nodes.filter(function(ele){
                    return ele.data("name") == select_node_name;
                });
                // ノードが存在するか確認し、処理
                if(select_node.data("name")){
                    if(id2relatedElements.get(select_node.data("name")).removed){
                        let ancestorsOfSelectnode = id2relatedElements.get(select_node.data("name")).ancestors
                        for(let i = ancestorsOfSelectnode.length -1; i > -1; i--){// ノードが格納されている場合，格納したディレクトリを上層から順に開くためデクリメントで処理
                            if(id2relatedElements.get(ancestorsOfSelectnode[i]).removed) restoreChildren(ancestorsOfSelectnode[i], cy.$(ancestorsOfSelectnode[i]), id2relatedElements)
                        }
                        $("#close").prop("disabled", false);
                        let allopen = true
                        directories.forEach(function(dir){
                            if(id2relatedElements.get(dir).removed) allopen = false;
                        })
                        if(allopen == true) $("#open").prop("disabled", true);
                    }
        
                    reset_elements_style(cy);
                    cy.$(select_node).addClass("selected");
                    highlight_select_elements(cy, select_node, ancestor_generations, descendant_generations);
                    $("#select_article").text("SELECT: " + select_node_name);
                    $(".color_index").removeClass("hidden_");
                    cy.center(select_node)
                    console.log(select_node)
                }
                else{
                    alert("ERROR: Don't have '" + select_node_name + "' node. Please select existed nodes.");
                }
    }
    
    
    // 強調表示したい祖先、子孫の世代数を取得
    $("#ancestor_generations").on("change", function(){
        ancestor_generations = $("#ancestor_generations").val();
        generation();
    });
    $("#descendant_generations").on("change", function(){
        descendant_generations = $("#descendant_generations").val();
        generation();
    });

    function generation(){
        if(cy.nodes(".selected").data()){
            let selected_node = cy.nodes().filter(function(ele){
                return ele.data("name") == cy.nodes(".selected").data("name");
            });
            reset_elements_style(cy);
            highlight_select_elements(cy, selected_node, ancestor_generations, descendant_generations);
        }
    }
    
    cy.on("clickElement", "node", function(event){
        if(!cy.$(this).hasClass("selected")){// クリックしたノードと，エッジで繋がるノードの色を変更
            if(!id2relatedElements.get(this.id()).removed) recursivelyRemove(this.id(), this, id2relatedElements)
            selection(event);
        }
    });

    function selection(event){
        // 全ノードをクラスから除外
        reset_elements_style(cy);
        // クリックしたノードをselectedクラスに入れる
        let clicked_node = event.target;
        highlight_select_elements(cy, clicked_node, ancestor_generations, descendant_generations);
        let clicked_node_name = clicked_node.data("name");
        $("#select_article").text("SELECT: " + clicked_node_name);
        $(".color_index").removeClass("hidden_");
    }

    // 背景をクリックしたときの処理
    cy.on("tap", function(event){
        let clicked_point = event.target;
        if (clicked_point === cy){
            reset_elements_style(cy);
            $(".color_index").addClass("hidden_");
        }
    });
    // エッジをクリックしたとき，グラフを初期状態のスタイルにする
    cy.edges().on("tap", function(event){
        reset_elements_style(cy);
        $(".color_index").addClass("hidden_");
    });
    
    // ノードの上にカーソルが来たとき，ノード名を表示する
    // jQuery.hoverを使うと動作が重くなるためmouseover/outを使用している
    cy.nodes().on("mouseover", function(cy_event){
        $(window).on("mousemove", function(window_event){ 
            document.getElementById("name-plate").style.top = window_event.clientY + (10) + "px";
            document.getElementById("name-plate").style.left = window_event.clientX + (10) +"px";
            if(!id2relatedElements.get(cy_event.target.data("id")).isParent){
                document.getElementById("name-plate").innerHTML = id2relatedElements.get(cy_event.target.data("id")).ancestors[0] + "<br>" + cy_event.target.data("name");
            }
        })
    });
    
    cy.nodes().on("mouseout", function(){
        $(window).on("mousemove", function(window_event){ 
            document.getElementById("name-plate").style.fontSize = ""
            document.getElementById("name-plate").innerHTML = "";
        })
    })
    
    /*ノードのタップ時の挙動*/
    let doubleClickDelayMs= 350; //ダブルクリックと認識するクリック間隔
    let previousTapStamp = 0;
    cy.nodes().on('tap', function(e) {
        let currentTapStamp= e.timeStamp;
        let msFromLastTap= currentTapStamp -previousTapStamp;
        if(id2relatedElements.get(e.target.id()).isParent){//複合親ノードであればダブルクリックかを判定
            if (msFromLastTap < doubleClickDelayMs && msFromLastTap > 0) {
                e.target.trigger('doubleTap', e);
            }
        }
        else if(!cy.$(e.target.id()).hasClass("selected")){// クリックしたノードの親と子、自身を色変更
            selection(e);
        }
        previousTapStamp= currentTapStamp;
        
    });
    
    //ダブルタップ
    cy.on('doubleTap', 'node', function(){ //フラグに応じて削除・復元
        let nodes = this;
        let id = nodes.data('id')
        if(cy.$(this).hasClass("selected")){
            reset_elements_style(cy);
            $(".color_index").addClass("hidden_");
        }
        
        if(id2relatedElements.get(id).removed == true){
            restoreNodes(openButton = false, id, nodes)
        } else{
            removeNodes(closeButton = false, id, nodes)
        }
    });

    //右クリック時の挙動
    cy.on('cxttap', 'node', function(e){
        document.getElementById("name-plate").style.fontSize = ""
        document.getElementById("name-plate").innerHTML = "";
        if(id2relatedElements.get(e.target.id()).isParent){
            contextMenu.showMenuItem('open/close')
            contextMenu.hideMenuItem('Go to Source Code')
            contextMenu.hideMenuItem('Highlight Same Cluster Nodes')
        }
        else {
            contextMenu.hideMenuItem('open/close')
            contextMenu.showMenuItem('Go to Source Code')
            contextMenu.showMenuItem('Highlight Same Cluster Nodes')
        }
    })

    //closeボタン押下時
    $("#close").click(function(){
        removeNodes(closeButton = true);
    })

    function removeNodes(closeButton, id, selectedNode){
        reset_elements_style(cy);
        $(".color_index").addClass("hidden_");
        $("#open").prop("disabled", false);
        if(closeButton){
            let bottom = -1;
            let removes = [];
            nodes.parent().forEach(function(node){// 表示されているディレクトリの内，最も深い層のものを探し全て非表示にする
                if(bottom < node.ancestors().length){
                    removes = [];
                    bottom = node.ancestors().length
                }
                if(bottom == node.ancestors().length){
                    removes.push(node)
                }
            })
            removes.forEach(function(remove){
                recursivelyRemove(remove.id(), remove, id2relatedElements)
            })
        }
        else recursivelyRemove(id, selectedNode, id2relatedElements);
        let allclose = true
        directories.forEach(function(dir){
            if(!id2relatedElements.get(dir).removed) allclose = false;
        })
        if(allclose == true) $("#close").prop("disabled", true);// 非表示にできるディレクトリがなければボタンを非アクティブ化する
    }

    //openボタン押下時
    $("#open").click(function(){
        restoreNodes(openButton = true)
    })

    function restoreNodes(openButton, id, selectedNode){
        $("#close").prop("disabled", false);
        if(openButton){
            $(".color_index").addClass("hidden_");
            cy.nodes().forEach(function(node){
                if(id2relatedElements.get(node.id()).removed && id2relatedElements.get(node.id()).isParent) {
                    restoreChildren(node.id(), node, id2relatedElements)
                }
            })
        }
        else restoreChildren(id, selectedNode, id2relatedElements)
        
        if(cy.nodes(".selected").data()){
            let selected_node = cy.nodes().filter(function(ele){
                return ele.data("name") == cy.nodes(".selected").data("name");
            });
            reset_elements_style(cy);
            highlight_select_elements(cy, selected_node, ancestor_generations, descendant_generations);
        }
        
        let allopen = true
        directories.forEach(function(dir){
            if(id2relatedElements.get(dir).removed) allopen = false;
        })
        if(allopen == true) $("#open").prop("disabled", true);// 全てのディレクトリが表示されていればボタンを非アクティブ化
    }

    // resetボタンでグラフを初期状態に戻す
    $(document).ready(function(){
        $("#reset").click(function(){
            location.reload();
        });
    });
    })

}, () => {
    alert("ERROR: Failed to read JSON file.");
});


/**
 * グラフの要素のスタイルを初期状態(ノード：赤い丸、エッジ：黒矢印)に戻す。
 * ただし、移動したノードの位置は戻らない。
 * @param {cytoscape object} cy グラフ本体
 * @return
**/
function reset_elements_style(cy) {
    let all_class_names = ["highlight",  "faded",  "selected", "interaction"];
    for(let i=0; i<10; i++){
        all_class_names.push("selected_ancestors" + i);
        all_class_names.push("selected_descendants" + i);
    }
    cy.elements().removeClass(all_class_names);
    cy.nodes().unlock();
}


/**
 * 選択されたノードとそのノードの親子を強調表示させる(selectedクラスに追加する)
 * @param {cytoscape object} cy グラフ本体
 * @param {cytoscape object} select_node cy内の単一のノード
 * @param {int} ancestor_generations 辿りたい祖先の数
 * @param {int} descendant_generations 辿りたい子孫の数
 * @return
**/
function highlight_select_elements(cy, select_node, ancestor_generations, descendant_generations){
    // 選択したノードの処理
    cy.$(select_node).addClass("highlight");
    cy.$(select_node).addClass("selected");

    // 選択したノードの祖先、子孫を強調表示する
    is_ancestor = true;
    highlight_connected_elements(cy, ancestor_generations, select_node, is_ancestor);
    highlight_connected_elements(cy, descendant_generations, select_node, !is_ancestor);

    // highlightクラス以外の物はfadedクラスに入れる
    fade_out_faded_elements(cy);

    // fadedクラスの物は、動かせないようにする
    cy.$(".faded").lock();

}


/**
 * 選択したノード(select_node)とその祖先または子孫を任意の世代数(generation)までを
 * 強調表示するクラスに追加する。
 * アルゴリズム
 *      次の処理を辿りたい世代数まで繰り返す
            1. first_connected_elementsの親(もしくは子)ノードとそのエッジを強調表示させるクラスに追加する
            2. 1でクラスに追加したノードをfirst_connected_elementsとして更新する
            3. 2でfirst_connected_elementsが空ならループを中断する
 * @param {cytoscape object} cy cytoscapeのグラフ本体
 * @param {int} generation 辿りたい世代数
 * @param {cytoscape object} select_node 選択したノード
 * @param {boolean} is_ancestor 辿りたいのは祖先かどうか。trueなら祖先、falseなら子孫を強調表示させていく。
 * @return
**/
function highlight_connected_elements(cy, generation, select_node, is_ancestor){
    let first_connected_elements = cy.collection();  // 親(もしくは子)を取得したいノードのコレクション（≒リスト）
    first_connected_elements = first_connected_elements.union(select_node);
    for (let i=0; i<generation; i++){
        let class_name = is_ancestor ? "selected_ancestors" : "selected_descendants";
        class_name += Math.min(4, i);
        let second_connected_elements = cy.collection();
        cy.$(first_connected_elements).forEach(function(n){
            let connect_elements = is_ancestor ? n.outgoers() : n.incomers();
            connect_elements = connect_elements.difference(cy.$(connect_elements).filter(".highlight"));
            cy.$(connect_elements).addClass("highlight");
            cy.$(connect_elements).nodes().addClass(class_name);
            second_connected_elements = second_connected_elements.union(connect_elements.nodes());
        });
        first_connected_elements = second_connected_elements;
        if (first_connected_elements.length === 0){
            break;
        }
    }
    cy.$(select_node).incomers().forEach(function(comer){
        for(let i=0; i<10; i++){
            if(comer.hasClass("selected_ancestors" + i)){
                comer.removeClass("selected_ancestors" + i)
                comer.addClass("interaction")
            }
        }
    })
}


/**
 * 強調表示されていない(highlightクラスに属していない)ノード、エッジをfadedクラスに入れる。
 * @param {cytoscape object} cy cytoscapeグラフ本体
 * @return
**/
// convert style to fade
function fade_out_faded_elements(cy){  // change_style_to_fade_for_not_selected_elements
    let other = cy.elements();
    other = other.difference(cy.elements(".highlight"));
    cy.$(other).addClass("faded");
}

/**
 * 子ノード群を非表示(処理上は削除)にする．
 * @param {string} id クリックされたノードのid
 * @param {cytoscape object} nodes 非表示にするノード群
 * @param {Map} id2relatedElements 全ノードのデータ
**/
function recursivelyRemove(id,nodes, id2relatedElements){
    let removingNodesList = [];
    for(;;){ //選択されたノードと子をリストに入れ、削除フラグを付ける
        nodes.forEach(function(node){
            id2relatedElements.get(node.data('id')).removed = true;
        });
        Array.prototype.push.apply(removingNodesList, nodes.children());
        // list.push()の場合，削除対象のノード群の配列が正しく生成できなかったためArrayを使用
        nodes = nodes.children();
        if( nodes.empty() ){ break; }
    }

    //当該サブグラフに関連するエッジ全てを一度削除する
    for( let x = removingNodesList.length - 1; x >= 0; x-- ){ //最下層のノードから処理し、順次削除
        let removeEdges = removingNodesList[x].connectedEdges();
        for(let y = 0; y < removeEdges.length; y++){ //エッジの削除・置き換え
            if(removeEdges[y].target().parent() != removeEdges[y].source().parent()){
                let replaceEdge = removeEdges[y];
                removeEdges[y].remove();
                
                let newSource;
                let newTarget;
                if(replaceEdge.target() == removingNodesList[x]){
                    newSource = replaceEdge.source().id();
                    newTarget = replaceEdge.target().parent().id();
                }
                else if(replaceEdge.source() == removingNodesList[x]){
                    newSource = replaceEdge.source().parent().id();
                    newTarget = replaceEdge.target().id();
                }
                if(newSource != newTarget)cy.add({group: 'edges', data:{id: replaceEdge.id(), source: newSource, target: newTarget}})
                // 最下層から処理するため，上の層の処理により将来的に削除されるエッジを作成する場合がある
            }
        }
        removingNodesList[x].remove();
    }
}


/**
 * 非表示となっている子ノード群を表示させる．
 * 内部的にはノードは削除されていたため，id2relatedElementsから子を取得し，再配置する．
 * @param {string} id クリックされたノードのid
 * @param {cytoscape object} nodes クリックされたノードそのもの
 * @param {Map} id2relatedElements 全ノードのデータ
**/
function restoreChildren(id, nodes, id2relatedElements){
    id2relatedElements.get(id).removed = false;
    id2relatedElements.get(id).children.restore(); //ノードを復元
  
    for(let x=0; x<id2relatedElements.get(id).edges.length; x++){ //エッジを順次復元
        let restoreEdge = id2relatedElements.get(id).edges[x];
        let restoreEdgeID = restoreEdge.id();
        
        //エッジを置き換える場合
        if(cy.$('#' + restoreEdgeID).length){
            if(restoreEdge.data('target') != cy.$('#' + restoreEdgeID).target().id() || restoreEdge.data('source') != cy.$('#' + restoreEdgeID).source().id()){
                cy.remove('#' + restoreEdgeID);
            }
        }
        
        if(cy.$(restoreEdge.source()).length * cy.$(restoreEdge.target()).length == 0 ){ //エッジの完全な復元ができない場合
            let newEnds = [];
            for(let i = 0; i < 2; i++){
                let origin = (i==0 ? restoreEdge.source().id() : restoreEdge.target().id()) //本来のソース・ターゲットを取得
                let ancestors = id2relatedElements.get(origin).ancestors
                for(let y = 0; y < ancestors.length; y++){
                    if(!id2relatedElements.get(ancestors[y]).removed){
                        if(y == 0)newEnds[i] = origin
                        else newEnds[i] = ancestors[y-1];
                        break;
                    }
                }
                if(ancestors.length == 0)newEnds[i] = origin;
                if(!newEnds[i])newEnds[i] = ancestors[ancestors.length-1]
                
            }
            let newSource = newEnds[0], newTarget = newEnds[1];

            if(newSource!=newTarget){ //自己ループでなければエッジを追加
                cy.add({group: 'edges', data:{id: restoreEdgeID, source: newSource, target: newTarget}})
            }
        }
        else{
            cy.add(id2relatedElements.get(id).edges[x])
        }
    }
}
  
// 2層分のリストを入力とする関数
function createAccordionMenu(level1, level2) {
    // parent_list変数に代入する値を格納する変数
    let menu = "";
    // レベル1の要素を順に処理する
    for (let key in level1) {
      // レベル1の要素の見出しを生成する
      let level1Item = document.createElement("details");
      let level1Summary = document.createElement("summary");
      level1Summary.textContent = level1[key];
      level1Item.appendChild(level1Summary);
      // レベル2の要素を順に処理する
      for (let subkey in level2[key]) {
        // レベル2の要素の見出しを生成する
        let level2Item = document.createElement("details");
        let level2Summary = document.createElement("summary");
        level2Summary.textContent = level2[key][subkey];
        level2Item.appendChild(level2Summary);
        // レベル2の要素の詳細を生成する
        let level2Detail = document.createElement("p");
        level2Detail.textContent = level2[key][subkey] + "の詳細";
        level2Item.appendChild(level2Detail);
        // レベル2の要素にスタイルを適用する
        level2Item.style.marginLeft = "20px";
        // レベル1の要素にレベル2の要素を追加する
        level1Item.appendChild(level2Item);
      }
      // menu変数にレベル1の要素を文字列に変換して追加する
      menu += level1Item.outerHTML;
    }
    // parent_list変数にmenu変数の値を代入する
    parent_list.innerHTML = menu;
  }
  