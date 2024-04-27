var nodes = new vis.DataSet([]);
var edges = new vis.DataSet([]);
var heuristic = {};
var selectedNodeId = null;
var selectedEdgeId = null;
var container = document.getElementById("mynetwork");
var nodeSelect = document.getElementById("nodeSelect");
var nodeSelect1 = document.getElementById("nodeSelect1");

var data = {
  nodes: nodes,
  edges: edges,
};

var options = {};
var network = new vis.Network(container, data, options);

var nodeIdCounter = 1;

function addNode() {
  // Use the counter as the new node ID
  var newNodeId = nodeIdCounter++;

  var newNodeLabel = "Node " + newNodeId;

  var nodeFont = {
    color: "white",
  };

  var newNode = {
    id: newNodeId,
    label: newNodeLabel + "\nh=1",
    color: "palevioletred",
    font: nodeFont,
    heuristic: 1,
  };

  // Check if the node with the same ID already exists
  if (nodes.get(newNodeId) === null) {
    nodes.add(newNode);
    heuristic[newNodeLabel] = newNode.heuristic;

    // Update the select dropdown with the names of every node
    updateNodeSelect();
    updateNodeSelect2();
    // Call the function to add checkboxes and options
  } else {
    console.error("Node with ID " + newNodeId + " already exists.");
  }
}

function updateNodeSelect() {
  var nodeOptions = nodes
    .get()
    .map(
      (node) =>
        `<option value="${node.label.split("\n")[0]}">${node.label}</option>`
    )
    .join("");
  nodeSelect.innerHTML = `<option value="0">Start:</option>${nodeOptions}`;
}
var goals = [];

function updateNodeSelect2() {
  var container = document.getElementById("customDropdown").querySelector("ul");
  container.innerHTML = "";

  var selectedNodeId = network.getSelectedNodes()[0];
  var selectedNode = nodes.get(selectedNodeId);

  if (selectedNode && selectedNode.label) {
    // Remove the deleted node's <li> element
    var deletedLi = container.querySelector(
      `li:has([id='${selectedNode.label.split("\n")[0]}'])`
    );
    if (deletedLi) {
      container.removeChild(deletedLi);
    }
  }

  var nodeOptions = nodes
    .get()
    .map(
      (node) =>
        `<li>
          <input type="checkbox" id="${
            node.label.split("\n")[0]
          }" class="custom-checkbox" />
          <label for="${node.label.split("\n")[0]}">${node.label}</label>
        </li>`
    )
    .join("");

  container.innerHTML = nodeOptions;

  var checkboxes = container.querySelectorAll(".custom-checkbox");
  checkboxes.forEach(function (checkbox) {
    checkbox.addEventListener("change", function () {
      if (this.checked) {
        this.parentElement.classList.add("checked");
        goals.push(this.id);
      } else {
        this.parentElement.classList.remove("checked");
        goals = goals.filter((goal) => goal !== this.id);
      }

      console.log(goals);
    });
  });
}

network.on("doubleClick", function (params) {
  if (params.nodes.length > 0) {
    if (!selectedNodeId) {
      selectedNodeId = params.nodes[0];
      customAlert("Source node selected. Now double click on the target node.");
    } else if (params.nodes[0] !== selectedNodeId) {
      var connectedNodeId = params.nodes[0];
      var newEdge = {
        from: selectedNodeId,
        to: connectedNodeId,
        label: "1",
        color: "#0969b8",
        width: 5,
        font: { size: 16 },
      };
      edges.add(newEdge);
      printNodeList();
      printEdgeList();
      selectedNodeId = null;
    }
  }
});

function editNode() {
  var selectedNodeId = network.getSelectedNodes()[0];
  if (selectedNodeId) {
    document.getElementById("myModal").style.display = "block";
    document.getElementById("newLabel").value = nodes
      .get(selectedNodeId)
      .label.split("\n")[0];
    document.getElementById("newHeuristic").value =
      heuristic[nodes.get(selectedNodeId).label.split("\n")[0]];
  } else {
    customAlert("Please select a node to edit.");
  }
}

function closeModal() {
  document.getElementById("myModal").style.display = "none";
}

function updateNodeLabelAndHeuristic() {
  var selectedNodeId = network.getSelectedNodes()[0];
  var newLabel = document.getElementById("newLabel").value;
  var newHeuristic = parseInt(document.getElementById("newHeuristic").value);

  if (selectedNodeId && newLabel.trim() !== "") {
    delete heuristic[nodes.get(selectedNodeId).label.split("\n")[0]];
    heuristic[newLabel] = newHeuristic;
    nodes.update({
      id: selectedNodeId,
      label: newLabel + "\nh=" + newHeuristic,
    });
    updateNodeSelect();
    updateNodeSelect2();
    closeModal();
  } else {
    alert("Invalid input. Please enter a valid label and heuristic value.");
  }
}

function editEdge() {
  var selectedEdgeId = network.getSelectedEdges()[0];
  if (selectedEdgeId) {
    document.getElementById("edgeModal").style.display = "block";
    clearEditEdgeInput();
  } else {
    customAlert("Please select an edge to edit.");
  }
}

function clearEditEdgeInput() {
  document.getElementById("newEdgeLabel").value = "";
}

function closeEdgeModal() {
  document.getElementById("edgeModal").style.display = "none";
}

function updateEdgeLabel() {
  var selectedEdgeId = network.getSelectedEdges()[0];
  var newEdgeLabel = document.getElementById("newEdgeLabel").value;

  if (selectedEdgeId && newEdgeLabel.trim() !== "") {
    edges.update({ id: selectedEdgeId, label: newEdgeLabel });
    closeEdgeModal();
  } else {
    alert("Invalid input. Please enter a valid label.");
  }
}

function solve() {
  var strategy = document.getElementById("strategy").value;
  var start = document.getElementById("nodeSelect").value;
  var nodeList = edges.get().map((edge) => ({
    from: nodes.get(edge.from).label.split("\n")[0],
    to: nodes.get(edge.to).label.split("\n")[0],
  }));

  var edgeList = edges.get().map((edge) => ({
    from: nodes.get(edge.from).label.split("\n")[0],
    to: nodes.get(edge.to).label.split("\n")[0],
    label: edge.label,
  }));
  // var start = nodeList[0].from;
  console.log("Node List:", nodeList);
  console.log("Edge List:", edgeList);
  console.log("Heuristic:", heuristic);
  console.log("Solving using strategy:", strategy, goals, start);
  fetch("http://127.0.0.1:5000/call_function", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      edge: nodeList,
      cost: edgeList,
      heuristic: heuristic,
      strategy: strategy,
      start: start,
      goal: goals,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      
      console.log("Result:", data.result);
      console.log("nodes",data.visited)
      var result=data.result;
      var visited= data.visited;
      colorNodesWithDelay(visited, 'grey', 3000);
      
      function findNodeByLabel(label) {
        return nodes.get().find(function (node) {
          return node.label.split("\n")[0] === label;
        });
      }
      
      
      
      function colorNodeByLabel(label, color) {
        var foundNode = findNodeByLabel(label);
        if (foundNode) {
          nodes.update({ id: foundNode.id, color: { background: color} });
        }
      }
      
      
      function colorNodesWithDelay(labels, color, delay) {
        labels.forEach(function (label, index) {
          setTimeout(function () {
            colorNodeByLabel(label, color);
      
            
            if (index === labels.length - 1) {
              
              setTimeout(function () {
                colorNodesWithDelay2(result, 'purple', 2000);
              }, 3000);
            }
          }, index * delay);
        });
      }
      function colorNodesWithDelay2(labels, color, delay) {
        labels.forEach(function (label, index, array) {
          // Exclude the last iteration from processing in the loop
          if (index < array.length - 1) {
            setTimeout(function () {
              colorNodeByLabel(label, color);
            }, index * delay);
          } else {
            // For the last iteration, process separately after the loop
            setTimeout(function () {
              colorNodeByLabel(label, color);
            }, index * delay);
          }
        });
      }
      
    })
    .catch((error) => console.error("Error:", error));
}







function customAlert(message) {
  var customAlertElement = document.getElementById("customAlert");
  customAlertElement.textContent = message;
  customAlertElement.style.display = "block";

  setTimeout(function () {
    customAlertElement.style.display = "none";
  }, 2000);
}

function deleteSelectedNode() {
  var selectedNodeId = network.getSelectedNodes()[0];

  if (selectedNodeId) {
    var selectedNode = nodes.get(selectedNodeId);

    if (selectedNode) {
      console.log("Deleting node:", selectedNode);

      // Remove all edges connected to the selected node
      var connectedEdges = edges.get({
        filter: (edge) =>
          edge.from === selectedNodeId || edge.to === selectedNodeId,
      });
      edges.remove(connectedEdges);

      // Remove the selected node
      nodes.remove({ id: selectedNodeId });

      delete heuristic[selectedNode.label.split("\n")[0]];

      // Find and remove the corresponding option from the dropdown
      var nodeSelect = document.getElementById("nodeSelect");

      // Remove from nodeSelect
      for (var i = 0; i < nodeSelect.options.length; i++) {
        if (nodeSelect.options[i].value === selectedNode.label.split("\n")[0]) {
          nodeSelect.remove(i);
          break;
        }
      }

      var customDropdown = document.getElementById("customDropdown");
      var goalsList = customDropdown.querySelector("ul");

      // Remove from goalsList
      var goalsListItems = goalsList.querySelectorAll("li");
      goalsListItems.forEach(function (item) {
        var checkboxValue = item.querySelector("input").value;
        if (checkboxValue === selectedNode.label.split("\n")[0]) {
          goalsList.removeChild(item);
        }
      });
      updateNodeSelect2();
    } else {
      customAlert("Selected node not found.");
    }
  } else {
    customAlert("Please select a node to delete.");
  }
}

function removeSelectedEdge() {
  var selectedEdgeId = network.getSelectedEdges()[0];
  if (selectedEdgeId) {
    edges.remove({ id: selectedEdgeId });
    printEdgeList();
  } else {
    customAlert("Please select an edge to remove.");
  }
}

function printNodeList() {
  var nodeListWithLabels = edges.get().map((edge) => ({
    from: nodes.get(edge.from).label.split("\n")[0],
    to: nodes.get(edge.to).label.split("\n")[0],
  }));
  console.log("Node List:", nodeListWithLabels);
}

function printEdgeList() {
  var edgeListWithLabels = edges.get().map((edge) => ({
    from: nodes.get(edge.from).label.split("\n")[0],
    to: nodes.get(edge.to).label.split("\n")[0],
    label: edge.label,
  }));
  console.log("Edge List:", edgeListWithLabels);
}

function printHeuristic() {
  console.log("Heuristic:", heuristic);
}
