// ==================== Info Didáctica de Compuertas ====================
const GateLogic = {
    'AND':  { func: (a, b) => a & b,            formula: 'A ∧ B', desc: 'Salida 1 solo si ambas entradas son 1.', tt: [[0,0,0],[0,1,0],[1,0,0],[1,1,1]] },
    'OR':   { func: (a, b) => a | b,            formula: 'A ∨ B', desc: 'Salida 1 si al menos una entrada es 1.', tt: [[0,0,0],[0,1,1],[1,0,1],[1,1,1]] },
    'NAND': { func: (a, b) => (a & b) ? 0 : 1,  formula: 'A ⊼ B', desc: 'Inverso de AND. Salida 0 solo si ambas son 1.', tt: [[0,0,1],[0,1,1],[1,0,1],[1,1,0]] },
    'NOR':  { func: (a, b) => (a | b) ? 0 : 1,  formula: 'A ⊽ B', desc: 'Inverso de OR. Salida 1 solo si ambas son 0.', tt: [[0,0,1],[0,1,0],[1,0,0],[1,1,0]] },
    'XOR':  { func: (a, b) => a ^ b,            formula: 'A ⊕ B', desc: 'Salida 1 si las entradas son diferentes.', tt: [[0,0,0],[0,1,1],[1,0,1],[1,1,0]] },
    'XNOR': { func: (a, b) => (a ^ b) ? 0 : 1,  formula: 'A ⊙ B', desc: 'Inverso de XOR. Salida 1 si entradas son iguales.', tt: [[0,0,1],[0,1,0],[1,0,0],[1,1,1]] }
};

// ==================== Modelos de Datos ====================
class Node {
    constructor(id, type, gateType, level, index, x, y) {
        this.id = id;
        this.type = type;          
        this.gateType = gateType;  
        this.level = level;        
        this.index = index;        
        this.x = x;
        this.y = y;
        this.value = 0;            
    }
}

class Connection {
    constructor(id, fromNode, toNode, toPort) {
        this.id = id;
        this.fromNode = fromNode;   
        this.toNode = toNode;       
        this.toPort = toPort;       
        this.value = 0;
    }
}

// ==================== Utils ====================
const sleep = ms => new Promise(r => setTimeout(r, ms));

// ==================== Controlador principal ====================
class TreeCircuitController {
    constructor() {
        // Elementos DOM
        this.container = document.getElementById('canvas-container');
        this.wireLayer = document.getElementById('wire-layer');
        this.nodeLayer = document.getElementById('node-layer');
        this.levelInput = document.getElementById('levelCount');
        this.generateBtn = document.getElementById('generateBtn');
        this.gatePanel = document.getElementById('gateTypePanel');
        this.inputTogglesDiv = document.getElementById('inputToggles');
        this.finalOutputDiv = document.getElementById('finalOutput');
        this.finalLight = document.getElementById('finalLight');
        
        // Flip-flop
        this.ffEnable = document.getElementById('ffEnable');
        this.ffInputsDiv = document.getElementById('ffInputs');
        this.ffOutputSpan = document.getElementById('ffOutput');
        this.ffStatusMsg = document.getElementById('ffStatusMsg');
        
        // Explicación
        this.evalLog = document.getElementById('evalLog');
        
        // Tooltip
        this.tooltip = document.getElementById('gateTooltip');
        this.ttTitle = document.getElementById('ttTitle');
        this.ttDesc = document.getElementById('ttDesc');
        this.ttBody = document.getElementById('ttBody');

        // Controles Canvas
        this.zoomInBtn = document.getElementById('zoomInBtn');
        this.zoomOutBtn = document.getElementById('zoomOutBtn');
        this.resetViewBtn = document.getElementById('resetViewBtn');

        // Estado del circuito
        this.nodes = new Map();          
        this.connections = new Map();    
        this.nextNodeId = 0;
        this.nextConnId = 0;
        this.nodesUI = new Map();        
        this.connectionsUI = new Map();  

        // Estado del flip-flop
        this.ffState = 0; 
        this.ffS = 0;
        this.ffR = 0;

        // Visualización y Animación
        this.isEvaluating = false;
        this.currentEvalCycle = 0;
        this.evalTimeout = null; 
        
        // Variables para interacción Canvas
        this.draggingNode = null;
        this.dragOffsetX = 0;
        this.dragOffsetY = 0;
        this.tempWire = null;            
        this.zoom = 1;
        this.panX = 0;
        this.panY = 0;
        this.isPanning = false;
        this.lastPanX = 0;
        this.lastPanY = 0;
        this.snapToGrid = true;
        this.gridSize = 20;

        this.initEvents();
        this.updateGateTypePanel(3); 
        this.generateTree(3);        
    }

    // ========== UI Setup ==========
    updateGateTypePanel(levels) {
        this.gatePanel.innerHTML = '';
        for (let lvl = 1; lvl <= levels; lvl++) {
            const div = document.createElement('div');
            div.className = 'gate-level';
            div.innerHTML = `
                <label>Nivel ${lvl}:</label>
                <select data-level="${lvl}">
                    <option value="AND">AND</option>
                    <option value="OR">OR</option>
                    <option value="NAND">NAND</option>
                    <option value="NOR">NOR</option>
                    <option value="XOR">XOR</option>
                    <option value="XNOR">XNOR</option>
                </select>
            `;
            div.querySelector('select').addEventListener('change', () => {
                this.generateTree(parseInt(this.levelInput.value));
            });
            this.gatePanel.appendChild(div);
        }
    }

    generateTree(levels) {
        this.clearAll();
        const gateTypes = Array.from(this.gatePanel.querySelectorAll('select')).map(sel => sel.value);
        const inputCount = Math.pow(2, levels);
        const inputNodes = [];
        
        for (let i = 0; i < inputCount; i++) {
            const node = new Node(this.nextNodeId++, 'input', null, 0, i, 0, 0);
            this.nodes.set(node.id, node);
            inputNodes.push(node);
        }

        const gateNodesByLevel = [];
        for (let lvl = 1; lvl <= levels; lvl++) {
            const gateCount = Math.pow(2, levels - lvl); 
            const levelGates = [];
            for (let i = 0; i < gateCount; i++) {
                const node = new Node(this.nextNodeId++, 'gate', gateTypes[lvl-1], lvl, i, 0, 0);
                this.nodes.set(node.id, node);
                levelGates.push(node);
            }
            gateNodesByLevel.push(levelGates);
        }

        for (let lvl = 0; lvl < levels; lvl++) {
            const currentGates = gateNodesByLevel[lvl]; 
            if (lvl === 0) {
                for (let g = 0; g < currentGates.length; g++) {
                    this.addConnection(inputNodes[g * 2].id, currentGates[g].id, 0);
                    this.addConnection(inputNodes[g * 2 + 1].id, currentGates[g].id, 1);
                }
            } else {
                const prevGates = gateNodesByLevel[lvl - 1];
                for (let g = 0; g < currentGates.length; g++) {
                    this.addConnection(prevGates[g * 2].id, currentGates[g].id, 0);
                    this.addConnection(prevGates[g * 2 + 1].id, currentGates[g].id, 1);
                }
            }
        }

        const startX = 80; const stepX = 200;
        const startY = 300; const stepY = 80;

        for (let i = 0; i < inputNodes.length; i++) {
            inputNodes[i].x = startX;
            inputNodes[i].y = startY + (i - (inputNodes.length-1)/2) * stepY;
        }

        for (let lvl = 0; lvl < levels; lvl++) {
            const gates = gateNodesByLevel[lvl];
            const level = lvl + 1; 
            const x = startX + level * stepX; 
            const currentStepY = stepY * Math.pow(2, level); 
            
            for (let i = 0; i < gates.length; i++) {
                const node = gates[i];
                node.x = x;
                node.y = startY + (i - (gates.length-1)/2) * currentStepY;
            }
        }

        this.nodes.forEach(node => this.createNodeUI(node));
        
        requestAnimationFrame(() => {
            this.connections.forEach(conn => this.createWireUI(conn));
            this.createInputToggles(inputNodes.length);
            this.resetView();
            this.triggerEvaluation(true);
        });
    }

    createInputToggles(count) {
        this.inputTogglesDiv.innerHTML = '';
        for (let i = 0; i < count; i++) {
            const toggle = document.createElement('div');
            toggle.className = 'input-toggle off';
            toggle.dataset.index = i;
            toggle.innerHTML = `I<sub>${i}</sub>: 0`;
            toggle.addEventListener('click', () => {
                const val = toggle.classList.contains('off') ? 1 : 0;
                toggle.classList.toggle('on', val === 1);
                toggle.classList.toggle('off', val === 0);
                toggle.innerHTML = `I<sub>${i}</sub>: ${val}`;
                
                const inputNode = Array.from(this.nodes.values()).find(n => n.type === 'input' && n.index === i);
                if (inputNode) {
                    inputNode.value = val;
                }
                
                this.scheduleEvaluation(); 
            });
            this.inputTogglesDiv.appendChild(toggle);
        }
    }

    // ========== Log & Animación Didáctica ==========
    clearLog() {
        this.evalLog.innerHTML = '';
    }
    
    addLog(htmlText, type = '') {
        const div = document.createElement('div');
        div.className = `log-entry ${type}`;
        div.innerHTML = htmlText;
        this.evalLog.appendChild(div);
        this.evalLog.scrollTop = this.evalLog.scrollHeight;
    }

    formatVal(v) {
        return `<span class="log-val-${v}">${v}</span>`;
    }

    scheduleEvaluation() {
        this.currentEvalCycle++; 
        this.isEvaluating = false; 
        
        this.clearLog();
        this.addLog('⏳ Recibiendo datos... Propagación en 2s', 'system');

        this.nodes.forEach(n => {
            if (n.type === 'gate') {
                n.value = 0;
                this.updateNodeValueUI(n);
            }
        });
        
        this.connections.forEach(c => {
            c.value = 0;
            const path = this.connectionsUI.get(c.id);
            if (path) {
                path.classList.remove('active');
                path.classList.add('inactive');
            }
        });
        
        this.nodes.forEach(n => {
            if (n.type === 'input') {
                this.updateNodeValueUI(n);
                this.updateOutgoingWires(n.id);
            }
        });

        if (this.evalTimeout) clearTimeout(this.evalTimeout);

        this.evalTimeout = setTimeout(() => {
            this.triggerEvaluation(false);
        }, 2000);
    }

    async triggerEvaluation(instant = false) {
        if (this.isEvaluating) return;
        this.isEvaluating = true;
        this.currentEvalCycle++;
        const cycle = this.currentEvalCycle;
        
        if (!instant) this.clearLog();
        if (!instant) this.addLog('Iniciando evaluación del circuito...', 'system');

        const levels = Math.max(...Array.from(this.nodes.values()).map(n => n.level)) + 1; 
        const nodesByLevel = Array.from({length: levels}, () => []);
        this.nodes.forEach(node => {
            if (node.type === 'input') node.level = 0;
            nodesByLevel[node.level].push(node);
        });

        nodesByLevel[0].forEach(node => {
            this.updateNodeValueUI(node);
            this.updateOutgoingWires(node.id);
        });

        for (let lvl = 1; lvl < levels; lvl++) {
            if (cycle !== this.currentEvalCycle) return; 
            
            if (!instant) await sleep(600);
            
            let levelLog = `<strong>Nivel ${lvl}</strong>:<br>`;
            const gates = nodesByLevel[lvl];
            
            for (let gate of gates) {
                const inputs = [0, 0];
                for (let conn of this.connections.values()) {
                    if (conn.toNode === gate.id) {
                        inputs[conn.toPort] = this.nodes.get(conn.fromNode).value;
                    }
                }
                
                const logic = GateLogic[gate.gateType];
                const out = logic.func(inputs[0], inputs[1]);
                gate.value = out;
                
                this.updateNodeValueUI(gate);
                if (!instant) {
                    const nodeUI = this.nodesUI.get(gate.id);
                    if (nodeUI) {
                        nodeUI.classList.remove('pulse-eval');
                        void nodeUI.offsetWidth; 
                        nodeUI.classList.add('pulse-eval');
                    }
                }
                
                this.updateOutgoingWires(gate.id);
                levelLog += `<span class="log-gate-formula">${logic.formula}</span> recibió (${this.formatVal(inputs[0])}, ${this.formatVal(inputs[1])}) ➔ Resultado = ${this.formatVal(out)}<br>`;
            }
            if (!instant) this.addLog(levelLog, 'level');
        }

        if (cycle !== this.currentEvalCycle) return;

        const root = nodesByLevel[levels-1][0];
        const circuitOutput = root ? root.value : 0;
        this.handleFlipFlop(circuitOutput, instant);
        
        if (!instant) this.addLog(`Evaluación completada.`, 'system');
        this.isEvaluating = false;
    }
    
    updateNodeValueUI(node) {
        const div = this.nodesUI.get(node.id);
        if (div) {
            const valSpan = div.querySelector('.node-value');
            if (valSpan) {
                valSpan.textContent = node.value;
                valSpan.classList.toggle('active', node.value === 1);
            }
        }
    }

    updateOutgoingWires(fromNodeId) {
        const fromNode = this.nodes.get(fromNodeId);
        this.connections.forEach(conn => {
            if (conn.fromNode === fromNodeId) {
                conn.value = fromNode.value;
                const path = this.connectionsUI.get(conn.id);
                if (path) {
                    path.classList.toggle('active', conn.value === 1);
                    path.classList.toggle('inactive', conn.value === 0);
                }
            }
        });
    }

    handleFlipFlop(circuitOut, instant) {
        if (this.ffEnable.checked) {
            this.ffS = parseInt(document.querySelector('.ff-toggle[data-ff="s"]').textContent);
            this.ffR = parseInt(document.querySelector('.ff-toggle[data-ff="r"]').textContent);
            
            let statusClass = 'normal';
            let statusText = 'Estado: Normal';

            if (this.ffS === 1 && this.ffR === 0) {
                this.ffState = 1;
                statusText = 'Set (Q=1)';
            } else if (this.ffS === 0 && this.ffR === 1) {
                this.ffState = 0;
                statusText = 'Reset (Q=0)';
            } else if (this.ffS === 1 && this.ffR === 1) {
                statusClass = 'error';
                statusText = 'Estado Inválido Detectado (S=1, R=1)';
            } else {
                statusClass = 'hold';
                statusText = 'Manteniendo Estado (Hold)';
            }
            
            this.ffStatusMsg.className = `ff-status-msg ${statusClass}`;
            this.ffStatusMsg.textContent = statusText;
            
            this.ffOutputSpan.textContent = this.ffState;
            this.finalOutputDiv.textContent = this.ffState;
            this.finalLight.classList.toggle('on', this.ffState === 1);
            this.finalLight.classList.toggle('off', this.ffState === 0);
            
            if(!instant) this.addLog(`Flip-Flop evaluado: ${statusText} ➔ Q=${this.formatVal(this.ffState)}`, 'result');
        } else {
            this.finalOutputDiv.textContent = circuitOut;
            this.finalLight.classList.toggle('on', circuitOut === 1);
            this.finalLight.classList.toggle('off', circuitOut === 0);
            if(!instant) this.addLog(`Salida de Árbol: ${this.formatVal(circuitOut)}`, 'result');
        }
    }

    // ========== Canvas & Nodes UI ==========
    createNodeUI(node) {
        const div = document.createElement('div');
        div.className = 'node';
        div.dataset.id = node.id;
        div.style.left = node.x + 'px';
        div.style.top = node.y + 'px';

        if (node.type === 'gate') {
            div.addEventListener('mouseenter', (e) => this.showTooltip(e, node.gateType));
            div.addEventListener('mouseleave', () => this.hideTooltip());
        }

        const img = document.createElement('img');
        if (node.type === 'input') {
            img.alt = 'IN'; img.style.display = 'none';
            div.innerHTML = `<div style="color:var(--text-muted); font-size:10px; margin-top:5px;">Entrada</div>`;
        } else if (node.type === 'gate') {
            img.src = `svg/${node.gateType.toLowerCase()}.svg`;
            img.alt = node.gateType;
            img.onerror = () => { img.style.display = 'none'; div.innerHTML = `<div style="font-weight:bold; color:white; margin-top:5px;">${node.gateType}</div>`; };
        }
        div.appendChild(img);
        
        if (node.type === 'gate') {
            const formSpan = document.createElement('span');
            formSpan.className = 'node-formula';
            formSpan.textContent = GateLogic[node.gateType].formula;
            div.appendChild(formSpan);
        }

        const valSpan = document.createElement('span');
        valSpan.className = 'node-value';
        valSpan.textContent = node.value;
        div.appendChild(valSpan);

        const portsDiv = document.createElement('div');
        portsDiv.className = 'ports';

        const inputPortsDiv = document.createElement('div');
        inputPortsDiv.className = 'input-ports';
        const inputCount = (node.type === 'gate') ? 2 : 0;
        for (let i = 0; i < inputCount; i++) {
            const port = document.createElement('div');
            port.className = 'port input';
            port.dataset.node = node.id; port.dataset.port = i; port.dataset.type = 'input';
            port.addEventListener('mousedown', (e) => this.onPortMouseDown(e, node.id, i, 'input'));
            inputPortsDiv.appendChild(port);
        }

        const outputPortDiv = document.createElement('div');
        outputPortDiv.className = 'output-port';
        const outPort = document.createElement('div');
        outPort.className = 'port output';
        outPort.dataset.node = node.id; outPort.dataset.port = 0; outPort.dataset.type = 'output';
        outPort.addEventListener('mousedown', (e) => this.onPortMouseDown(e, node.id, 0, 'output'));
        outputPortDiv.appendChild(outPort);

        portsDiv.appendChild(inputPortsDiv);
        portsDiv.appendChild(outputPortDiv);
        div.appendChild(portsDiv);

        div.addEventListener('mousedown', (e) => {
            if (e.target && e.target.classList && e.target.classList.contains('port')) return;
            e.preventDefault();
            this.draggingNode = node;
            const rect = this.container.getBoundingClientRect();
            this.dragOffsetX = (e.clientX - rect.left - this.panX) / this.zoom - node.x;
            this.dragOffsetY = (e.clientY - rect.top - this.panY) / this.zoom - node.y;
        });

        this.nodeLayer.appendChild(div);
        this.nodesUI.set(node.id, div);
    }

    showTooltip(e, gateType) {
        const info = GateLogic[gateType];
        if(!info) return;
        this.ttTitle.textContent = `Compuerta ${gateType}`;
        this.ttDesc.innerHTML = `<strong>Fórmula:</strong> ${info.formula}<br>${info.desc}`;
        
        this.ttBody.innerHTML = '';
        info.tt.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${row[0]}</td><td>${row[1]}</td><td class="tt-out-${row[2]}">${row[2]}</td>`;
            this.ttBody.appendChild(tr);
        });

        this.tooltip.classList.remove('hidden');
        const rect = e.target.getBoundingClientRect();
        this.tooltip.style.left = (rect.right + 10) + 'px';
        this.tooltip.style.top = rect.top + 'px';
    }
    
    hideTooltip() { 
        this.tooltip.classList.add('hidden'); 
    }

    createWireUI(conn) {
        const fromPos = this.getPortPosition(this.nodes.get(conn.fromNode), 'output', 0);
        const toPos = this.getPortPosition(this.nodes.get(conn.toNode), 'input', conn.toPort);
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.classList.add('wire', 'inactive');
        path.setAttribute('d', this.computeWirePath(fromPos.x, fromPos.y, toPos.x, toPos.y));
        path.dataset.id = conn.id;
        this.wireLayer.appendChild(path);
        this.connectionsUI.set(conn.id, path);
        return path;
    }

    addConnection(fromNodeId, toNodeId, toPort) {
        const conn = new Connection(this.nextConnId++, fromNodeId, toNodeId, toPort);
        this.connections.set(conn.id, conn);
        return conn;
    }

    updateWire(connId) {
        const conn = this.connections.get(connId);
        if (!conn) return;
        const path = this.connectionsUI.get(connId);
        const fromPos = this.getPortPosition(this.nodes.get(conn.fromNode), 'output', 0);
        const toPos = this.getPortPosition(this.nodes.get(conn.toNode), 'input', conn.toPort);
        path.setAttribute('d', this.computeWirePath(fromPos.x, fromPos.y, toPos.x, toPos.y));
    }
    
    updateAllWires() { 
        this.connections.forEach((_, id) => this.updateWire(id)); 
    }

    // SOLUCIÓN MATEMÁTICA PURA: Evita errores de DOM y garantiza conexiones irrompibles
    getPortPosition(node, portType, portIndex) {
        if (portType === 'output') {
            return { x: node.x + 80, y: node.y + 59 };
        } else {
            const offsetY = (portIndex === 0) ? 46 : 78;
            return { x: node.x, y: node.y + offsetY };
        }
    }

    computeWirePath(x1, y1, x2, y2) {
        const dx = Math.abs(x2 - x1);
        const ctrlX = x1 + dx * 0.5;
        return `M ${x1} ${y1} C ${ctrlX} ${y1}, ${ctrlX} ${y2}, ${x2} ${y2}`;
    }

    onPortMouseDown(e, nodeId, portIndex, portType) {
        e.stopPropagation();
        if (portType === 'output') {
            const pos = this.getPortPosition(this.nodes.get(nodeId), 'output', 0);
            const tempPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            tempPath.classList.add('wire', 'temp');
            tempPath.setAttribute('d', this.computeWirePath(pos.x, pos.y, pos.x, pos.y));
            this.wireLayer.appendChild(tempPath);
            this.tempWire = { fromNode: nodeId, fromX: pos.x, fromY: pos.y, path: tempPath };
        }
    }

    // ========== Eventos Globales ==========
    initEvents() {
        this.container.addEventListener('wheel', (e) => {
            e.preventDefault();
            const delta = e.deltaY > 0 ? 0.9 : 1.1;
            this.doZoom(delta, e.clientX, e.clientY);
        });

        this.zoomInBtn.addEventListener('click', () => this.doZoom(1.2));
        this.zoomOutBtn.addEventListener('click', () => this.doZoom(0.8));
        this.resetViewBtn.addEventListener('click', () => this.resetView());

        // SOLUCIÓN A PRUEBA DE FALLOS: Verificación segura del clic
        this.container.addEventListener('mousedown', (e) => {
            if (e.target instanceof Element) {
                if (e.target.closest('.node')) return;
                if (e.target.classList.contains('port')) return;
            }

            e.preventDefault();
            this.isPanning = true;
            this.lastPanX = e.clientX;
            this.lastPanY = e.clientY;
        });

        window.addEventListener('mousemove', (e) => {
            if (this.isPanning) {
                this.panX += e.clientX - this.lastPanX;
                this.panY += e.clientY - this.lastPanY;
                this.lastPanX = e.clientX;
                this.lastPanY = e.clientY;
                this.applyTransform();
            }

            if (this.draggingNode) {
                const rect = this.container.getBoundingClientRect();
                let x = (e.clientX - rect.left - this.panX) / this.zoom - this.dragOffsetX;
                let y = (e.clientY - rect.top - this.panY) / this.zoom - this.dragOffsetY;
                
                if (this.snapToGrid) { 
                    x = Math.round(x/this.gridSize)*this.gridSize; 
                    y = Math.round(y/this.gridSize)*this.gridSize; 
                }
                
                this.draggingNode.x = x; 
                this.draggingNode.y = y;
                
                const div = this.nodesUI.get(this.draggingNode.id);
                if (div) { 
                    div.style.left = x + 'px'; 
                    div.style.top = y + 'px'; 
                }
                this.updateAllWires();
            }

            if (this.tempWire) {
                const rect = this.container.getBoundingClientRect();
                const mx = (e.clientX - rect.left - this.panX) / this.zoom;
                const my = (e.clientY - rect.top - this.panY) / this.zoom;
                this.tempWire.path.setAttribute('d', this.computeWirePath(this.tempWire.fromX, this.tempWire.fromY, mx, my));
            }
        });

        window.addEventListener('mouseup', (e) => {
            this.isPanning = false;
            this.draggingNode = null;
            
            if (this.tempWire) {
                // Validación para conectar cables
                const els = document.elementsFromPoint(e.clientX, e.clientY);
                const target = els.find(el => el.classList && el.classList.contains('port') && el.dataset.type === 'input');
                
                if (target && parseInt(target.dataset.node) !== this.tempWire.fromNode) {
                    const toNodeId = parseInt(target.dataset.node);
                    const toPort = parseInt(target.dataset.port);
                    for (let [id, c] of this.connections) {
                        if (c.toNode === toNodeId && c.toPort === toPort) {
                            this.connections.delete(id);
                            const p = this.connectionsUI.get(id);
                            if(p) p.remove();
                            this.connectionsUI.delete(id);
                        }
                    }
                    const newConn = this.addConnection(this.tempWire.fromNode, toNodeId, toPort);
                    this.createWireUI(newConn);
                    
                    this.scheduleEvaluation();
                }
                this.tempWire.path.remove();
                this.tempWire = null;
            }
        });

        this.generateBtn.addEventListener('click', () => {
            const levels = parseInt(this.levelInput.value);
            this.updateGateTypePanel(levels);
            this.generateTree(levels);
        });
        
        this.levelInput.addEventListener('change', () => {
            this.updateGateTypePanel(parseInt(this.levelInput.value));
        });

        this.ffEnable.addEventListener('change', (e) => {
            if (e.target.checked) this.ffInputsDiv.classList.remove('hidden');
            else this.ffInputsDiv.classList.add('hidden');
            this.scheduleEvaluation();
        });

        document.querySelectorAll('.ff-toggle').forEach(toggle => {
            toggle.addEventListener('click', () => {
                const val = toggle.classList.contains('off') ? 1 : 0;
                toggle.classList.toggle('on', val === 1);
                toggle.classList.toggle('off', val === 0);
                toggle.textContent = val;
                this.scheduleEvaluation();
            });
        });
    }

    doZoom(factor, cx, cy) {
        const rect = this.container.getBoundingClientRect();
        
        // Coordenadas de mouse seguras
        const centerX = typeof cx === 'number' ? cx : rect.left + rect.width / 2;
        const centerY = typeof cy === 'number' ? cy : rect.top + rect.height / 2;
        
        const mouseX = centerX - rect.left;
        const mouseY = centerY - rect.top;
        
        const newZoom = Math.min(Math.max(this.zoom * factor, 0.3), 3);
        
        this.panX = mouseX - (mouseX - this.panX) * (newZoom / this.zoom);
        this.panY = mouseY - (mouseY - this.panY) * (newZoom / this.zoom);
        this.zoom = newZoom;
        
        this.applyTransform();
    }
    
    // VISUAL FEEDBACK: Aquí aplicamos el paneo incluso a la cuadrícula de fondo
    applyTransform() {
        // Fallbacks por si algún número falla mágicamente
        if (isNaN(this.panX)) this.panX = 0;
        if (isNaN(this.panY)) this.panY = 0;
        if (isNaN(this.zoom)) this.zoom = 1;

        this.nodeLayer.style.transform = `translate(${this.panX}px, ${this.panY}px) scale(${this.zoom})`;
        this.wireLayer.style.transform = `translate(${this.panX}px, ${this.panY}px) scale(${this.zoom})`;
        
        // Efecto visual profundo: mover la cuadrícula para acompañar el mapa
        this.container.style.backgroundPosition = `${this.panX}px ${this.panY}px`;
        this.container.style.backgroundSize = `${20 * this.zoom}px ${20 * this.zoom}px`;
    }

    resetView() {
        this.zoom = 0.8;
        this.panX = 50;
        this.panY = 50;
        this.applyTransform();
    }

    clearAll() {
        if (this.evalTimeout) clearTimeout(this.evalTimeout);
        this.currentEvalCycle++;
        this.isEvaluating = false;

        this.nodes.clear(); this.connections.clear();
        this.nodesUI.forEach(div => div.remove()); this.connectionsUI.forEach(path => path.remove());
        this.nodesUI.clear(); this.connectionsUI.clear();
        this.nextNodeId = 0; this.nextConnId = 0;
    }
}

document.addEventListener('DOMContentLoaded', () => new TreeCircuitController());