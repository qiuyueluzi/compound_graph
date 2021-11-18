
/*
createGraph.pyで出力されたファイルとcytoscape.jsを使って
グラフの描画を行う
*/
$(function(){
    $.when(
        $.getJSON('./graph_attrs/compound_dot_graph.json')
    )
    .then((dot_graph) => {
        $.when(
            $.getJSON('./graph_attrs/mml_classification.json')
        )
        .then((classification) =>{
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
            
            const directory = new Set();
            for(let x=0; x<classification["mml_classification"].length; x++){
                let parents = classification.mml_classification[x]["directory"].split('/')
                let parentsName = new String();
                for(let y = 1; y < parents.length; y++){
                    let idName = parents[1];
                    let parentDirectory = new String();
                    for(let z = 2; z < y + 1; z++){
                        parentDirectory = idName;
                        idName += '/' + parents[z];
                    }
                    let isAlready = directory.size;
                    directory.add(idName)
                    if(isAlready != directory.size){
                        let displayName = idName.split('/').slice(-1)
                        if(y == 1) cy.add({group: 'nodes', data: {id: idName, name: displayName}});
                        else cy.add({group: 'nodes', data: {id: idName, name: displayName, parent: parentDirectory}})
                    }
                    parentsName = idName
                }
                dot_graph.eleObjs[x].data["parent"] = parentsName;
            }
            console.log(dot_graph)
            cy.add(dot_graph["eleObjs"]);
        
            
            const childrenData = new Map(); //サブグラフに含まれるノードを記録する
            const edgesData = new Map();
            let nodes = cy.nodes();
            let edges = cy.edges();
            for(let x = 0; x < nodes.length; x++){ //初期状態での全ノードの、子ノードと関連するエッジの情報を記録
                let curNode = cy.$(nodes[x]);
                let id = curNode.data('id');
                
                let childrenNodes = curNode.children(); //当ノードの子ノード
                let connectedEdges = curNode.connectedEdges(); //当ノードに接続するエッジ
                let connectedChildEdges = curNode.descendants().connectedEdges(); //当ノードの子ノードに接続するエッジ
                let parentNode = nodes[x].data('parent'); //当ノードの親ノード
                
                if(childrenNodes.length > 0)curNode.style({
                    'shape': 'square',
                    'color': '#000000'
                }); //子ノードを持つノード(サブグラフ)は形を変更(閉じた際に反映されている)
                
                childrenData.set(id, {node :childrenNodes, edge: connectedEdges.union(connectedChildEdges), parent: parentNode, removed: false});
            }
            for(let x = 0; x < edges.length; x++){ //初期状態での全エッジのソースとターゲットを記録
                let curEdge = cy.$(edges[x]);
                let id = curEdge.data('id');
                let curTarget = curEdge.target();
                let curSource = curEdge.source();
                
                edgesData.set(id, {source: curSource, target: curTarget});
            }
            console.log(childrenData)
            nodes.forEach(function(node){ //
                //if(node.isOrphan())recursivelyRemove(node.id(), node)
            })
            let layout = cy.elements().layout({
                name: "klay",
                spacingFactor: 12
            })
            layout.run()
            console.log(cy.zoom())

            

            // Set graph style
            cy.style([
                /* 初期状態のスタイル */
                {
                    selector: "node",
                    css: {"background-color": "#000000", "shape": "ellipse", "width": "150", "height": "150",
                    "content": "data(name)", "font-size": 40, "opacity": 1, "z-index": 1,
                    "text-halign":"center", "text-valign": "center", "font-style": "normal",
                    "font-weight": "bold", "color": "#bd20a0",
                    "text-outline-color": "#FFFFFF", "text-outline-opacity": 1, "text-outline-width": 10}  // 0.8 30
                },
                {
                    selector: 'node:parent',
                    css: {
                            'content': 'data(name)',
                            'font-size': 900,
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
                    "target-arrow-color": "black", "arrow-scale": 3, "width": 5, "opacity": 0.3, "z-index": 1}  //0.3
                },
                /* ノードが左クリックされたときに適応されるスタイル */
                // 選択されたノード全てのスタイル
                {
                    selector: "node.highlight",
                    css: {"font-size": 20,  "width": 250, "height": 250, "font-size": 100,
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
            css: {"background-color": "#ff0000", "color": "#ffffff",
            "text-outline-color": "#ff0000", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors1",
                css: {"background-color": "#ff4400", "color": "#ffffff",
                "text-outline-color": "#ff4400", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors2",
                css: {"background-color": "#ff7700", "color": "#ffffff",
                "text-outline-color": "#ff7700", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors3",
                css: {"background-color": "#ff9900",  "color": "#ffffff",
                "text-outline-color": "#ff9900", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors4",
                css: {"background-color": "#ffbb00",  "color": "#ffffff",
                "text-outline-color": "#ffbb00", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            // 選択された(強調表示する)子孫のスタイル
            {
                selector: "node.selected_descendants0",
                css: {"background-color": "#0000ff", "color": "#ffffff",
                "text-outline-color": "#0000ff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants1",
                css: {"background-color": "#0077ff", "color": "#ffffff",
                "text-outline-color": "#0077ff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants2",
                css: {"background-color": "#00bbff", "color": "#ffffff",
                "text-outline-color": "#00bbff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants3",
                css: {"background-color": "#00ddff", "color": "#000000",
                "text-outline-color": "#00ddff", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants4",
                css: {"background-color": "#00ffff", "color": "#000000",
                "text-outline-color": "#00ffff", "text-outline-opacity": 1, "text-outline-width": 10}
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
        let ancestor = nodes.ancestors();
        let orphan = nodes.orphans();
        fontsize(ancestor, orphan);
        
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
                $(".color_index").removeClass("hidden_show");
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
                $(".color_index").addClass("hidden_show");
            }
        });
        // エッジをクリックしたとき，グラフを初期状態のスタイルにする
        cy.edges().on("tap", function(event){
            reset_elements_style(cy);
            $(".color_index").addClass("hidden_show");
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
        cy.nodes().on("cxttap", function(event){
            try {  // your browser may block popups
                window.open(this.data("href"));
            } catch(e){  // fall back on url change
                window.location.href = this.data("href");
            }
        });


        let doubleClickDelayMs= 350; //ダブルクリックと認識するクリック間隔
        let previousTapStamp = 0;
        cy.nodes().on('tap', function(e) {
            let currentTapStamp= e.timeStamp;
            let msFromLastTap= currentTapStamp -previousTapStamp;
            if(childrenData.get(e.target.id()).node.length > 0){//複合親ノードであればダブルクリックかを判定
                if (msFromLastTap < doubleClickDelayMs && msFromLastTap > 0) {
                    e.target.trigger('doubleTap', e);
                }
            }
            else{// クリックしたノードの親と子、自身を色変更
                // 全ノードをクラスから除外
                reset_elements_style(cy);
                // クリックしたノードをselectedクラスに入れる
                let clicked_node = e.target;
                highlight_select_elements(cy, clicked_node, ancestor_generations, descendant_generations);
                let clicked_node_name = clicked_node.data("name");
                $("#select_article").text("SELECT: " + clicked_node_name);
                $(".color_index").removeClass("hidden_show");
            }
            previousTapStamp= currentTapStamp;
            
        });
        
        cy.on('doubleTap', 'node', function(){ //フラグに応じて削除・復元
            let nodes = this;
            let id = nodes.data('id')
            
            if(childrenData.get(id).removed == true){
                restoreChildren(id, nodes, childrenData, edgesData);
                if(cy.nodes(".selected").data()){
                    let selected_node = cy.nodes().filter(function(ele){
                        return ele.data("name") == cy.nodes(".selected").data("name");
                    });
                    reset_elements_style(cy);
                    highlight_select_elements(cy, selected_node, ancestor_generations, descendant_generations);
                }
            } else{
                recursivelyRemove(id, nodes, childrenData);
                reset_elements_style(cy);
                $(".color_index").addClass("hidden_show");
            }
            fontsize(ancestor, orphan);
            
            console.log('finish')
            
        });


        cy.on('zoom', function(e){
            console.log(cy.zoom())
            fontsize(ancestor, orphan);
        })
        
        
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



function restoreChildren(id, nodes, childrenData, edgesData){ //複合ノードを復元する
    childrenData.get(id).removed = false;
    childrenData.get(id).node.restore(); //子ノードを復元
  
    for(let x=0; x<childrenData.get(id).edge.length; x++){
        let restoreEdge = childrenData.get(id).edge[x]; //引数のnodesに関連する全てのエッジを一つずつ復元対象にしていく
        let restoreEdgeID = childrenData.get(id).edge[x].id(); //復元エッジのID
        
        if(cy.$('#' + restoreEdgeID).target() != undefined && cy.$('#' + restoreEdgeID).source() != undefined){
            if(edgesData.get(restoreEdgeID).target != cy.$('#' + restoreEdgeID).target().id() || edgesData.get(restoreEdgeID).source != cy.$('#' + restoreEdgeID).source().id()){
                //idが重複するエッジを生成しようとした場合に、当該エッジが初期状態と異なる状態であれば実行される
                
                cy.remove('#' + restoreEdgeID); //重複している現存エッジを消去する
                console.log('remove Edge ' + restoreEdgeID)
                x--; //ループ変数を減らしもう一度同じエッジの追加を行う
            }
        }
        else if(cy.$(restoreEdge.source()).length * cy.$(restoreEdge.target()).length == 0 ){ //復元エッジの両端どちらかが表示されていない場合、lengthが0になる
            console.log('try restore:'+restoreEdgeID)
            let newSource = edgesData.get(restoreEdgeID).source.id(); //復元エッジのソース、ターゲットを取得
            let newTarget = edgesData.get(restoreEdgeID).target.id();
            let sFlag = (childrenData.get(childrenData.get(newSource).parent) == undefined ? false : childrenData.get(childrenData.get(newSource).parent).removed); 
            let tFlag = (childrenData.get(childrenData.get(newTarget).parent) == undefined ? false : childrenData.get(childrenData.get(newTarget).parent).removed); 
            //ソース、ターゲットの親のremoveを取得
            //removeがfalseであればnewソース、ターゲットは表示されている
            //ただし、初期状態から最上部のサブグラフを指していたエッジなどは親を読み込めないので三項演算子で弾く
            
            while(sFlag || tFlag){
                if(sFlag){ //親が閉じられているなら復元エッジのソースをその親に置き換え、更にその親のremoveを取得
                    //親が表示されているノード(removeがfalseであるサブグラフ)が得られるまで登り続ける
                    try{
                        newSource = childrenData.get(newSource).parent;
                        sFlag = childrenData.get(childrenData.get(newSource).parent).removed;
                    }
                    catch(error){sFlag = false;} //親がそれ以上居ない場合.parentを読み込めないためフラグを書き換える
                }
                
                if(tFlag){
                    try{
                        newTarget = childrenData.get(newTarget).parent;
                        tFlag = childrenData.get(childrenData.get(newTarget).parent).removed;
                    }
                    catch(error){tFlag = false;}
                }
                
            }
            if(newSource!=newTarget){ //自己ループにならないならエッジを追加
                cy.add({group: 'edges', data:{id: restoreEdgeID, source: newSource, target: newTarget}})
                console.log('create Edge ' + restoreEdgeID)
            }
        }
        else{
            cy.add(childrenData.get(id).edge[x]) //ノードに関連するエッジを復元、ただしソースかターゲットが存在しない場合があるのでエラーを捕捉する
            console.log(childrenData.get(id).edge[x].id() + ' : restore')
        }
    }
}
  

function recursivelyRemove(id,nodes, childrenData){ //複合ノードを閉じる
    let toRemove = [];
    for(;;){
        nodes.forEach(function(node){ //選択されたノードと子のremoveフラグを全てtrueにする
            childrenData.get(node.data('id')).removed = true;
        });
        Array.prototype.push.apply(toRemove, nodes.children()); //削除する全ての子ノードをプッシュ
        nodes = nodes.children();
        if( nodes.empty() ){ break; }
    }

    for( let i = toRemove.length - 1; i >= 0; i-- ){ //当該サブグラフに関連するエッジ全てを一度削除する
        let remEdge = toRemove[i].connectedEdges();
        for(let j = 0; j < remEdge.length; j++){
            if(remEdge[j].target().parent() != remEdge[j].source().parent()){ //他のサブグラフを跨ぐエッジ(ソースとターゲットの親が別のエッジ)は置き換える
            let replaceEdge = remEdge[j]; //removeを行うエッジ(remEdge[j])はremove後は参照できないので別の変数に記録する
            remEdge[j].remove();
  
            let newSource; //ソース、ターゲットのうち削除される方は親に置き換える
            let newTarget;
            if(replaceEdge.target() == toRemove[i]){
                newSource = replaceEdge.source().id();
                newTarget = replaceEdge.target().parent().id();
            }
            else if(replaceEdge.source() == toRemove[i]){
                newSource = replaceEdge.source().parent().id();
                newTarget = replaceEdge.target().id();
            }
            if(newSource != newTarget)cy.add({group: 'edges', data:{id: replaceEdge.id(), source: newSource, target: newTarget}})
            } //親しか参照してないけど何故か孫以下のエッジも丸ごと削除しても、ちゃんと表示されてる一番上の親に置き換わる
        }  //最下層から順に消してて、都度1段ずつ上に置き換えられてるのかしら　よくわかんないです
        toRemove[i].remove();
    }
}

function fontsize(ancestor, orphan){
    if((cy.zoom() <= 0.05)){
        cy.style().selector('node').style({
            'font-size': 0
        })
        cy.style().selector('node.highlight').style({
            'font-size': 20 / cy.zoom()
        })
        cy.style().selector(ancestor).style({
            'font-size': 0
        })
        cy.style().selector(ancestor&&orphan).style({
            'font-size': 25 / cy.zoom()
        })
        .update()
    }
    else if((cy.zoom() > 0.05) && (cy.zoom() <= 0.07)){
        cy.style().selector('node').style({
            'font-size': 0
        })
        cy.style().selector('node.highlight').style({
            'font-size': 20 / cy.zoom()
        })
        cy.style().selector(ancestor).style({
            'font-size': 20 / cy.zoom()
        })
        cy.style().selector(ancestor&&orphan).style({
            'font-size': 25 / cy.zoom()
        })
        .update()
    }
    else if(cy.zoom() > 0.07){
        cy.style().selector('node').style({
            'font-size': 15 / cy.zoom()
        })
        cy.style().selector('node.highlight').style({
            'font-size': 20 / cy.zoom()
        })
        cy.style().selector(ancestor).style({
            'font-size': 20 / cy.zoom()
        })
        cy.style().selector(ancestor&&orphan).style({
            'font-size': 25 / cy.zoom()
        })
        .update()
    }
}
