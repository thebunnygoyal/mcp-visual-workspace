#!/usr/bin/env python3
"""
Obsidian Canvas to GitHub Visual Converter
Converts .canvas files to interactive HTML for GitHub Pages
"""

import json
import sys
import os
from pathlib import Path

def convert_canvas_to_html(canvas_file):
    """Convert Obsidian .canvas file to interactive HTML"""
    
    # Read canvas file
    with open(canvas_file, 'r') as f:
        canvas_data = json.load(f)
    
    # HTML template with enhanced styling
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Converted from Obsidian Canvas</title>
    <style>
        body {{
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            overflow: auto;
        }}
        
        #canvas {{
            position: relative;
            width: max-content;
            min-width: 100vw;
            min-height: 100vh;
            background: 
                radial-gradient(circle at 20% 50%, #1e293b 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, #1e3a5f 0%, transparent 50%),
                #0d1117;
        }}
        
        .canvas-node {{
            position: absolute;
            background: rgba(30, 41, 59, 0.9);
            border: 2px solid #38bdf8;
            border-radius: 8px;
            padding: 16px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}
        
        .canvas-node:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(56, 189, 248, 0.4);
        }}
        
        .canvas-node h3 {{
            margin: 0 0 8px 0;
            color: #38bdf8;
        }}
        
        .canvas-edge {{
            position: absolute;
            pointer-events: none;
            z-index: -1;
        }}
        
        .info {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(30, 41, 59, 0.9);
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #38bdf8;
            backdrop-filter: blur(10px);
            max-width: 300px;
        }}
    </style>
</head>
<body>
    <div id="canvas">
        <svg id="edges" style="position: absolute; width: 100%; height: 100%; z-index: -1;"></svg>
        {nodes}
    </div>
    
    <div class="info">
        <h3>📊 Canvas Statistics</h3>
        <p>Nodes: {node_count}</p>
        <p>Connections: {edge_count}</p>
        <p>Converted from: {filename}</p>
    </div>
    
    <script>
        // Draw edges
        const edges = {edges_json};
        const svg = document.getElementById('edges');
        
        edges.forEach(edge => {{
            const fromEl = document.getElementById(edge.from);
            const toEl = document.getElementById(edge.to);
            
            if (fromEl && toEl) {{
                const fromRect = fromEl.getBoundingClientRect();
                const toRect = toEl.getBoundingClientRect();
                
                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line.setAttribute('x1', fromRect.left + fromRect.width / 2);
                line.setAttribute('y1', fromRect.top + fromRect.height / 2);
                line.setAttribute('x2', toRect.left + toRect.width / 2);
                line.setAttribute('y2', toRect.top + toRect.height / 2);
                line.setAttribute('stroke', '#38bdf8');
                line.setAttribute('stroke-width', '2');
                line.setAttribute('opacity', '0.5');
                svg.appendChild(line);
            }}
        }});
    </script>
</body>
</html>"""
    
    # Process nodes
    nodes_html = []
    for node in canvas_data.get('nodes', []):
        node_type = node.get('type', 'text')
        x = node.get('x', 0)
        y = node.get('y', 0)
        width = node.get('width', 250)
        height = node.get('height', 100)
        node_id = node.get('id', '')
        
        content = ''
        if node_type == 'text':
            content = node.get('text', '')
        elif node_type == 'file':
            content = f"📄 {node.get('file', 'File')}"  
        elif node_type == 'link':
            content = f"🔗 {node.get('url', 'Link')}"
        
        node_html = f'''<div class="canvas-node" id="{node_id}" 
            style="left: {x}px; top: {y}px; width: {width}px; min-height: {height}px;">
            {content}
        </div>'''
        
        nodes_html.append(node_html)
    
    # Process edges
    edges_data = []
    for edge in canvas_data.get('edges', []):
        edges_data.append({
            'from': edge.get('fromNode', ''),
            'to': edge.get('toNode', '')
        })
    
    # Generate final HTML
    html = html_template.format(
        title=Path(canvas_file).stem,
        nodes='\n'.join(nodes_html),
        node_count=len(canvas_data.get('nodes', [])),
        edge_count=len(canvas_data.get('edges', [])),
        filename=Path(canvas_file).name,
        edges_json=json.dumps(edges_data)
    )
    
    # Write output file
    output_file = Path(canvas_file).with_suffix('.html')
    with open(output_file, 'w') as f:
        f.write(html)
    
    return output_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python canvas-converter.py <canvas-file>")
        print("Converts Obsidian .canvas files to interactive HTML")
        sys.exit(1)
    
    canvas_file = sys.argv[1]
    
    if not os.path.exists(canvas_file):
        print(f"Error: File '{canvas_file}' not found")
        sys.exit(1)
    
    if not canvas_file.endswith('.canvas'):
        print("Error: File must have .canvas extension")
        sys.exit(1)
    
    try:
        output_file = convert_canvas_to_html(canvas_file)
        print(f"✅ Successfully converted to: {output_file}")
        print(f"📊 View your interactive canvas in any web browser")
    except Exception as e:
        print(f"❌ Error converting canvas: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()