
/*
createGraph.pyで出力されたファイルとcytoscape.jsを使って
グラフの描画を行う
*/
$(function(){
    $.when(
        $.getJSON('./graph_attrs/graph_class.json')
    )
    .then((dot_graph) => {
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
    
        let directories = [];
        for(let x = 0; x < dot_graph["parents"].length; x++){ //ディレクトリ一覧を作成
            directories[x] = dot_graph.parents[x].data["id"];
        }
        
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
        for(let x = 0; x < nodes.length; x++){ //初期状態での全ノードの、関連するエッジの情報を記録
            let currentNode = cy.$(nodes[x]);
            let id = currentNode.data('id');
            
            let childrenNodes = currentNode.children();
            let connectedEdges = currentNode.connectedEdges();
            let childConnectedEdges = currentNode.descendants().connectedEdges();
            let parentNode = currentNode.data('parent');

            let ancestorNodes = []
            currentNode.ancestors().forEach(function(ancestor){
                ancestorNodes.push(ancestor.id())  //各ノードの祖先を記録
            });
            ancestorNodes.sort();
            ancestorNodes.reverse(); 
            
            let isParent = false;
            if(childrenNodes.length > 0){
                isParent = true;
                currentNode.style({
                    'shape': 'square',
                    "width": "200", "height": "200",
                    'color': '#000000',
                    "text-outline-color": '#FFFFFF',
                    'text-valign': 'top',
                }); //selectorによる一括指定では変更できなかったため，個別に親ディレクトリのスタイル指定を行う
            }
            
            id2relatedElements.set(id, {
                children :childrenNodes, 
                edges: connectedEdges.union(childConnectedEdges), 
                parent: parentNode, 
                ancestors: ancestorNodes, 
                isParent: isParent, 
                removed: false
            });
        }

        let layout = cy.elements().layout({ //klayレイアウトを適用
            name: "klay",
            spacingFactor: 10
        })
        layout.run()

        let contextMenu = cy.contextMenus({ //右クリック時のコンテキストメニュー
            evtType: ['cxttap'],
            menuItems: [
              {
                id: 'select',
                content: 'select',
                tooltipText: 'select',
                selector: 'node',
                onClickFunction: (event) => {
                  event.target.trigger("clickElement", event);
                },
                hasTrailingDivider: true,
              },
              {
                id: 'link',
                content: 'link',
                tooltipText: 'link',
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
              }
            ],
          });


        // Set graph style
        cy.style([
            /* 初期状態のスタイル */
            {
                selector: "node",
                css: {"background-color": "#000000", "shape": "ellipse", "width": "150", "height": "150",
                "content": "data(name)", 'font-size': 80, "opacity": 1, "z-index": 1,
                "text-halign":"center", "text-valign": "center", "font-style": "normal",
                "font-weight": "bold", "color": "#FFFFFF",
                "text-outline-color": "#000000", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: 'node:parent',
                css: {
                        'content': 'data(name)',
                        'font-size': 200,
                        "text-outline-color": '#FFFFFF',
                        'color': '#000000',
                        'text-valign': 'top',
                        'text-halign': 'center',
                        'background-color': '#20bd3d',
                        'background-opacity': 0.25
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
            "text-outline-color": "#99ff00", "text-outline-opacity": 1, "text-outline-width": 10
        }
    },
    // 選択された(強調表示する)祖先のスタイル
    {
        selector: "node.selected_ancestors0", 
        css: {"background-color": "#ffbb00", "color": "#ffffff",
        "text-outline-color": "#ffbb00", "text-outline-opacity": 1, "text-outline-width": 10}
        },
        {
            selector: "node.selected_ancestors1",
            css: {"background-color": "#ff9900", "color": "#ffffff",
            "text-outline-color": "#ff9900", "text-outline-opacity": 1, "text-outline-width": 10}
        },
        {
            selector: "node.selected_ancestors2",
            css: {"background-color": "#ff7700", "color": "#ffffff",
            "text-outline-color": "#ff7700", "text-outline-opacity": 1, "text-outline-width": 10}
        },
        {
            selector: "node.selected_ancestors3",
            css: {"background-color": "#ff4400",  "color": "#ffffff",
            "text-outline-color": "#ff4400", "text-outline-opacity": 1, "text-outline-width": 10}
        },
        {
            selector: "node.selected_ancestors4",
            css: {"background-color": "#ff0000",  "color": "#ffffff",
            "text-outline-color": "#ff0000", "text-outline-opacity": 1, "text-outline-width": 10}
        },
        // 選択された(強調表示する)子孫のスタイル
        {
            selector: "node.selected_descendants0",
            css: {"background-color": "#00ffff", "color": "#ffffff",
            "text-outline-color": "#00ffff", "text-outline-opacity": 1, "text-outline-width": 10}
        },
        {
            selector: "node.selected_descendants1",
            css: {"background-color": "#00ddff", "color": "#ffffff",
            "text-outline-color": "#00ddff", "text-outline-opacity": 1, "text-outline-width": 10}
        },
        {
            selector: "node.selected_descendants2",
            css: {"background-color": "#00bbff", "color": "#ffffff",
            "text-outline-color": "#00bbff", "text-outline-opacity": 1, "text-outline-width": 10}
        },
        {
            selector: "node.selected_descendants3",
            css: {"background-color": "#0077ff", "color": "#000000",
            "text-outline-color": "#0077ff", "text-outline-opacity": 1, "text-outline-width": 10}
        },
        {
            selector: "node.selected_descendants4",
            css: {"background-color": "#0000ff", "color": "#000000",
            "text-outline-color": "#0000ff", "text-outline-opacity": 1, "text-outline-width": 10}
        },
        {
            selector: "node.interaction",
            css: {"background-color": "#ff00ff", "color": "#ffffff",
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
        }

    ]);
    
    /* 初期状態の設定 */
    all_nodes_positions = cy.nodes().positions();  //ノードの位置を記録　今のところ使ってない
    cy.fit(cy.nodes().orphans());
    let allAncestors = nodes.ancestors();
    let allOrphans = nodes.orphans();
    cy.style().selector(allAncestors&&allOrphans).style({
        'font-size': 350
    })
    .update()
    $("#open").prop("disabled", true);
    
    // 強調表示する祖先、子孫の世代数の初期化
    let ancestor_generations = 1;
    let descendant_generations = 1;
    
    /* 検索機能の追加 */
    // 全ノード名の取得
    let all_article_names = [];
    let all_parent_names = [];
    nodes.orphans().forEach(function(parent){
        if(parent.isParent())all_parent_names.push(parent.data("name"));
        function childrenPush(parent, level){
            parent.children().forEach(function(child){
                if(child.isParent())all_parent_names.push("-"+child.data("name"));
                if(child.children())childrenPush(child, level++);
            })
        }
        childrenPush(parent, 1)

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
    for (let parent_name of all_parent_names){
        $("#parent_list").append($("<option/>").val(parent_name).html(parent_name));
    }

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
            if(!id2relatedElements.get(cy_event.target.data("id")).isParent)document.getElementById("name-plate").innerHTML = cy_event.target.data("name");
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
        if(id2relatedElements.get(e.target.id()).isParent){
            contextMenu.showMenuItem('open/close')
            contextMenu.hideMenuItem('link')
        }
        else {
            contextMenu.hideMenuItem('open/close')
            contextMenu.showMenuItem('link')
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
  
