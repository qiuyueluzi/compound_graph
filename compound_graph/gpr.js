/**
 * 子ノード群を非表示(処理上は削除)にする．
 * @param {string} id クリックされたノードのid
 * @param {cytoscape object} nodes 非表示にするノード群
 * @param {Map} id2relatedElements 全ノードのデータ
**/
function recursivelyRemove(id, nodes, id2relatedElements) {
    let removingNodesList = [];
    
    while (nodes.nonempty()) {
      nodes.forEach(function(node) {
        id2relatedElements.get(node.data('id')).removed = true;
      });
      
      removingNodesList.push(...nodes.children());
      nodes = nodes.children();
    }
  
    for (let x = removingNodesList.length - 1; x >= 0; x--) {
      let removeEdges = removingNodesList[x].connectedEdges();
  
      for (let y = 0; y < removeEdges.length; y++) {
        let replaceEdge = removeEdges[y];
        
        if (replaceEdge.target().parent() != replaceEdge.source().parent()) {
          replaceEdge.remove();
          
          let newSource, newTarget;
          
          if (replaceEdge.target() == removingNodesList[x]) {
            newSource = replaceEdge.source().id();
            newTarget = replaceEdge.target().parent().id();
          } else if (replaceEdge.source() == removingNodesList[x]) {
            newSource = replaceEdge.source().parent().id();
            newTarget = replaceEdge.target().id();
          }
          
          if (newSource != newTarget) {
            cy.add({ group: 'edges', data: { id: replaceEdge.id(), source: newSource, target: newTarget } });
          }
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
  function restoreChildren(id, nodes, id2relatedElements) {
    let relatedElement = id2relatedElements.get(id);
    relatedElement.removed = false;
    relatedElement.children.restore();
  
    for (let x = 0; x < relatedElement.edges.length; x++) {
      let restoreEdge = relatedElement.edges[x];
      let restoreEdgeID = restoreEdge.id();
      let existingEdge = cy.$('#' + restoreEdgeID);
  
      if (existingEdge.length && (restoreEdge.data('target') != existingEdge.target().id() || restoreEdge.data('source') != existingEdge.source().id())) {
        existingEdge.remove();
      }
  
      if (cy.$(restoreEdge.source()).length * cy.$(restoreEdge.target()).length === 0) {
        let newEnds = [];
  
        for (let i = 0; i < 2; i++) {
          let origin = (i === 0 ? restoreEdge.source().id() : restoreEdge.target().id());
          let ancestors = id2relatedElements.get(origin).ancestors;
  
          for (let y = 0; y < ancestors.length; y++) {
            if (!id2relatedElements.get(ancestors[y]).removed) {
              if (y === 0) {
                newEnds[i] = origin;
              } else {
                newEnds[i] = ancestors[y - 1];
              }
  
              break;
            }
          }
  
          if (ancestors.length === 0) {
            newEnds[i] = origin;
          }
  
          if (!newEnds[i]) {
            newEnds[i] = ancestors[ancestors.length - 1];
          }
        }
  
        let newSource = newEnds[0], newTarget = newEnds[1];
  
        if (newSource !== newTarget) {
          cy.add({ group: 'edges', data: { id: restoreEdgeID, source: newSource, target: newTarget } });
        }
      } else {
        cy.add(relatedElement.edges[x]);
      }
    }
  }