/*
createGraph.pyで出力されたファイルとcytoscape.jsを使って
グラフの描画を行う
*/
$(function(){
    $.when(
        $.getJSON('./graph_attrs/dot_graph_hits_authority.json'),
        $.getJSON('./graph_attrs/sfdp_graph_hits_authority.json'),
        $.getJSON('./graph_attrs/dot_graph_hits_hub.json'),
        $.getJSON('./graph_attrs/sfdp_graph_hits_hub.json'),
        $.getJSON('./graph_attrs/dot_graph_pagerank.json'),
        $.getJSON('./graph_attrs/sfdp_graph_pagerank.json'),
    )
    .then((dot_graph_auth, sfdp_graph_auth, dot_graph_hub, sfdp_graph_hub, dot_graph_pagerank, sfdp_graph_pagerank) => {
        // cytoscapeグラフの作成(初期化)
        let cy = window.cy = cytoscape({
            container: document.getElementById('graph'),
            elements: [],
            boxSelectionEnabled: true,
            autounselectify: false,
            selectionType: "additive",
            wheelSensitivity: 0.1
        });
        let graph = {};
        if(layout==='dot_auth'){
            graph = dot_graph_auth[0];
        }
        else if(layout==='sfdp_auth'){
            graph = sfdp_graph_auth[0];
        }
        else if(layout==='dot_hub'){
            graph = dot_graph_hub[0];
        }
        else if(layout==='sfdp_hub'){
            graph = sfdp_graph_hub[0];
        }
        else if(layout==='dot_pagerank'){
            graph = dot_graph_pagerank[0];
        }
        else{
            graph = sfdp_graph_pagerank[0];
        }

        let nodes = graph["elements"]["nodes"];
        let edges = graph["elements"]["edges"];
        let nodes_and_edges = [];
    
        for(let i in nodes){
            for(let j in nodes[i]){
                let node = {};
                node["group"] = "nodes";
                node["data"] = {"id": nodes[i][j]["id"], "name": nodes[i][j]["name"], 
                                "href": nodes[i][j]["href"], "ranking": nodes[i][j]["ranking"],
                                "group": nodes[i][j]["group"]};
                node["position"] = {"x": (nodes[i][j]["x"] + 1) * 300, "y": (nodes[i][j]["y"] + 1) * 300};
                nodes_and_edges.push(node);
            }
        }
        for(let i in edges){
            for(let j in edges[i]){
                let edge = {};
                edge["group"] = "edges";
                edge["data"] = {"source":edges[i][j]["source"], "target":edges[i][j]["target"]};
                nodes_and_edges.push(edge);
            }
        }
        cy.add(nodes_and_edges);
        // Set graph style
        cy.style([
            /* 初期状態のスタイル */
            {
                selector: "node",
                css: {"shape": "ellipse", "width": "250", "height": "250",
                      "content": "data(name)", "font-size": 40, "opacity": 1, "z-index": 1,
                      "text-halign":"center", "text-valign": "center", "font-style": "normal",
                      "font-weight": "bold", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node[group=9]", 
                css: {"background-color": "#0000ff", "color": "#ffffff", 
                      "text-outline-color": "#0000ff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node[group=8]", 
                css: {"background-color": "#4477ff", "color": "#ffffff", 
                      "text-outline-color": "#4477ff", "text-outline-opacity": 1, "text-outline-width": 10}
            },            
            {
                selector: "node[group=7]", 
                css: {"background-color": "#99bbff", "color": "#000000", 
                      "text-outline-color": "#99bbff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node[group=6]", 
                css: {"background-color": "#bbffff", "color": "#000000", 
                      "text-outline-color": "#bbffff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node[group=5]",
                css: {"background-color": "#ddffff", "color": "#000000",
                      "text-outline-color": "#ddffff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node[group=4]", 
                css: {"background-color": "#ffdddd", "color": "#000000", 
                      "text-outline-color": "#ffdddd", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node[group=3]", 
                css: {"background-color": "#ffbbbb", "color": "#000000",
                      "text-outline-color": "#ffbbbb", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node[group=2]", 
                css: {"background-color": "#ff9999", "color": "#000000",
                      "text-outline-color": "#ff9999", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node[group=1]", 
                css: {"background-color": "#ff7777", "color": "#ffffff",
                      "text-outline-color": "#ff7777", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node[group=0]", 
                css: {"background-color": "#ff0000", "color": "#ffffff",
                      "text-outline-color": "#ff0000", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "edge",
                css: {"line-color": "black", "target-arrow-shape": "triangle", "curve-style": "straight",
                "target-arrow-color": "black", "arrow-scale": 3, "width": 5, "opacity": 0.3, "z-index": 1}
            },
            // 強調表示されたノードをつなぐエッジのスタイル
            {
                selector: "edge.highlight",
                css: {"line-color": "#006400", "curve-style": "straight",
                "target-arrow-color": "#006400", "arrow-scale": 5, "width": 7, "opacity": 1, "z-index": 20}
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
            }
        ]);

        /* 初期状態の設定 */
        all_nodes_positions = cy.nodes().positions();  //ノードの位置を記録　今のところ使ってない
        let all_nodes = cy.nodes();
        let all_elements = cy.elements();
        cy.fit(cy.nodes().orphans());


        // 強調表示する祖先、子孫の世代数の初期化
        let ancestor_generations = 1;
        let descendant_generations = 1;


        /* 検索機能の追加 */
        // 全ノード名の取得
        let all_article_names = [];
        cy.nodes("[!is_dummy]").forEach(function(node){
            all_article_names.push(node.data("name"));
        });
        all_article_names.sort();
        // datalistに全ノード名を追加
        for (let article_name of all_article_names){
            $("#article_list").append($("<option/>").val(article_name).html(article_name));
        }
        // searchボタンをクリックしたら検索開始
        $("#search").click(function() {
            // dropdownで選択したノード名、または記述したノード名を取得
            let select_node_name = $("#article_name").val();
            let select_node = cy.nodes().filter(function(ele){
                return ele.data("name") == select_node_name;
            });
            // ノードが存在するか確認し、処理
            if(select_node.data("name")){
                reset_elements_style(cy);
                cy.$(select_node).addClass("selected");
                highlight_select_elements(cy, select_node, ancestor_generations, descendant_generations);
                $("#select_article").text("SELECT: " + select_node_name);
            }
            else{
                alert("ERROR: Don't have '" + select_node_name + "' node. Please select existed nodes.");
            }
        });
        // 入力が終わった時も検索を開始する
        $("#article_name").change(function() {
            // dropdownで選択したノード名、または記述したノード名を取得
            let select_node_name = $("#article_name").val();
            let select_node = cy.nodes().filter(function(ele){
                return ele.data("name") == select_node_name;
            });
            // ノードが存在するか確認し、処理
            if(select_node.data("name")){
                reset_elements_style(cy);
                cy.$(select_node).addClass("selected");
                highlight_select_elements(cy, select_node, ancestor_generations, descendant_generations);
                $("#select_article").text("SELECT: " + select_node_name);
                $(".color_index").removeClass("hidden_show");
            }
        });


        // 強調表示したい祖先、子孫の世代数を取得
        $("#ancestor_generations").on("change", function(){
            ancestor_generations = $("#ancestor_generations").val();
        });
        $("#descendant_generations").on("change", function(){
            descendant_generations = $("#descendant_generations").val();
        });


        // 背景をクリックしたときの処理
        cy.on("tap", function(event){
            let clicked_point = event.target;
            if (clicked_point === cy){
                reset_elements_style(cy);
            }
        });
        // エッジをクリックしたとき，グラフを初期状態のスタイルにする
        cy.edges().on("tap", function(event){
            reset_elements_style(cy);
        });


        // ノードの上にカーソルが来たとき，ノード名を表示する
        $(window).on("mousemove", function(window_event){ 
            cy.nodes().on("mouseover", function(cy_event){
                document.getElementById("name-plate").style.top = window_event.clientY + (10) + "px";
                document.getElementById("name-plate").style.left = window_event.clientX + (10) +"px";
                document.getElementById("name-plate").textContent = cy_event.target.data("name");
            });
            cy.nodes().on("mouseout", function(){
                document.getElementById("name-plate").textContent = "";
            })
        });


        // ノードをクリックした場合、リンクに飛ぶ(htmlリンクの設定)
        // faded状態ならば反応しない
        cy.nodes().on("cxttap", function(event){
            let clicked_node = event.target;
            try {  // your browser may block popups
                window.open(this.data("href"));
            } catch(e){  // fall back on url change
                window.location.href = this.data("href");
            }
        });


        // クリックしたノードの親と子、自身を色変更
        cy.nodes().on("tap", function(e){
            // 全ノードをクラスから除外
            reset_elements_style(cy);
            // クリックしたノードをselectedクラスに入れる
            let clicked_node = e.target;
            highlight_select_elements(cy, clicked_node, ancestor_generations, descendant_generations);
            let clicked_node_name = clicked_node.data("name");
            $("#select_article").text("SELECT: " + clicked_node_name);
        });
        

        // re-highlightボタンで再度ハイライトする
        $("#re-highlight").click(function() {
            if(cy.nodes(".selected").data()){
                let selected_node = cy.nodes().filter(function(ele){
                    return ele.data("name") == cy.nodes(".selected").data("name");
                });
                reset_elements_style(cy);
                highlight_select_elements(cy, selected_node, ancestor_generations, descendant_generations);
            }
        });


        // resetボタンでリロードにする
        $(document).ready(function(){
            $("#reset").click(function(){
                location.reload();
            });
        });

    }, () => {
        alert("ERROR: Failed to read JSON file.");
    });

});


/**
 * グラフの要素のスタイルを初期状態(ノード：赤い丸、エッジ：黒矢印)に戻す。
 * ただし、移動したノードの位置は戻らない。
 * @param {cytoscape object} cy グラフ本体
 * @return
**/
function reset_elements_style(cy) {
    let all_class_names = ["highlight",  "faded",  "selected"];
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
        let second_connected_elements = cy.collection();
        cy.$(first_connected_elements).forEach(function(n){
            let connect_elements = is_ancestor ? n.outgoers() : n.incomers();
            connect_elements = connect_elements.difference(cy.$(connect_elements).filter(".highlight"));
            cy.$(connect_elements).addClass("highlight");
            second_connected_elements = second_connected_elements.union(connect_elements.nodes());
        });
        first_connected_elements = second_connected_elements;
        if (first_connected_elements.length === 0){
            break;
        }
    }
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
