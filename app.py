import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx

st.title("📖 The Handmaid's Tale Explorer")
st.markdown("An interactive toolkit for exploring Margaret Atwood’s *The Handmaid's Tale* through data, design, and AI.")

# Sidebar navigation
page = st.sidebar.radio("Choose a view", ["Tension Graph", "Metaphors", "Similes", "Heatmap", "Character", "Character Web"])

# --- Data Setup ---
chapters = [
    (1, 5),  (2, 6),  (3, 6),  (4, 8),
    (5, 7),  (6, 9),  (7, 6),  (8, 10),
    (9, 7),  (10, 8), (11, 9),  (12, 10)
]
df = pd.DataFrame(chapters, columns=['Chapter', 'Tension'])
df['Label'] = 'Chapter ' + df['Chapter'].astype(str)

event_map = {
    'Chapter 1': "🔴 Offred's Introduction to Gilead",
    'Chapter 2': "💔 The Ceremony",
    'Chapter 3': "📝 Offred's Rebellion Begins",
    'Chapter 4': "👁️ Eyes Everywhere: Surveillance",
    'Chapter 5': "🔥 The Escape Attempt"
}
df['Event'] = df['Label'].map(event_map)

# --- Tension Graph View ---
if page == "Tension Graph":
    st.subheader("📈 Scene-by-Scene Tension in The Handmaid's Tale")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Label'],
        y=df['Tension'],
        mode='lines+markers',
        line=dict(color='#C71585', width=3),
        marker=dict(size=8, color='#C71585', line=dict(width=1, color='white')),
        hovertemplate='<b>%{x}</b><br>Tension: %{y}<extra></extra>',
        name='Tension'
    ))

    for _, row in df.iterrows():
        if pd.notna(row['Event']):
            fig.add_annotation(
                x=row['Label'],
                y=row['Tension'],
                text=row['Event'],
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40,
                font=dict(size=12, color='black'),
                arrowcolor="#C71585",
                bgcolor="white",
                bordercolor="#C71585",
                borderwidth=1,
                opacity=0.9
            )

    fig.update_layout(
        xaxis_title='Chapter',
        yaxis_title='Tension (1–10)',
        xaxis=dict(tickangle=45),
        template='plotly_white',
        height=600,          # Keep the height as is
        width=1200,          # Increase the width for more room
        margin=dict(l=40, r=40, t=60, b=150),
    )

    st.plotly_chart(fig, use_container_width=True)

# --- Metaphors ---
elif page == "Metaphors":
    st.subheader("🧠 Metaphors in The Handmaid's Tale")

    metaphors = [
        ("Chapter 1", "“Better never means better for everyone... It always means worse, for some.”"),
        ("Chapter 2", "“A rat in a maze is free to go anywhere, as long as it stays inside the maze.”"),
        ("Chapter 3", "“Ignoring isn’t the same as ignorance, you have to work at it.”"),
        ("Chapter 5", "“Nolite te bastardes carborundorum.”")
    ]

    for chapter, quote in metaphors:
        st.markdown(f"**{chapter}**  \n> *{quote}*")

# --- Similes ---
elif page == "Similes":
    st.subheader("🪞 Similes in The Handmaid's Tale")

    similes = [
        ("Chapter 1", "“Her eyes were like pools of sorrow.”"),
        ("Chapter 2", "“The world outside is changing, just like the seasons.”"),
        ("Chapter 4", "“Her hands are like ice, but she is still warm on the inside.”"),
        ("Chapter 6", "“Like a cracked mirror, everything in this world is distorted.”")
    ]

    for chapter, quote in similes:
        st.markdown(f"**{chapter}**  \n> *{quote}*")

# --- Heatmap ---
elif page == "Heatmap":
    st.subheader("🌡️ Tension Heatmap in The Handmaid's Tale")

    # Adding a finer granularity (e.g., Chapter and Sub-Chapter or use more granular points)
    # For simplicity, here we simulate more granular data with sub-chapters
    granular_chapters = [
        (1, 1, 5), (1, 2, 6), (1, 3, 7), (2, 1, 6), (2, 2, 8), (3, 1, 7), (3, 2, 5), (4, 1, 7),
        (5, 1, 6), (5, 2, 9), (6, 1, 7), (6, 2, 6), (7, 1, 7), (8, 1, 8), (9, 1, 6), (10, 1, 9)
    ]
    
    df_granular = pd.DataFrame(granular_chapters, columns=['Chapter', 'Sub-Chapter', 'Tension'])
    df_granular['Label'] = df_granular['Chapter'].astype(str) + '.' + df_granular['Sub-Chapter'].astype(str)

    # Reshaping data for heatmap
    tension_matrix = df_granular.pivot_table(index="Chapter", columns="Sub-Chapter", values="Tension")

    # Plotting the heatmap with a red-to-blue color scale and more granularity
    fig = go.Figure(data=go.Heatmap(
        z=tension_matrix.values,
        x=tension_matrix.columns,
        y=tension_matrix.index,  
        colorscale='RdBu',  # Red to Blue color scale
        colorbar=dict(title="Tension (1–10)"),
        hovertemplate="Tension: %{z}<extra></extra>"
    ))

    fig.update_layout(
        title="Chapter-by-Chapter Tension Heatmap",
        title_x=0.5,
        xaxis_title="Sub-Chapter",
        yaxis_title="Chapter",
        xaxis=dict(
            tickmode='array',
            tickvals=tension_matrix.columns,
            tickangle=45,
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(0,0,0,0.1)',  # Light gridlines
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=tension_matrix.index,
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(0,0,0,0.1)',  # Light gridlines
            tickfont=dict(size=12)
        ),
        height=700,
        width=1200,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        margin=dict(l=50, r=50, t=80, b=100),
        template='plotly_dark'  # Dark mode theme
    )

    st.plotly_chart(fig, use_container_width=True)


# --- Character Insights ---
elif page == "Character":
    st.subheader("🎭 Character Insights")

    # Dropdown to select a character
    character = st.selectbox("Choose a character", ["Offred", "The Commander", "Serina Joy", "Moira", "Ofglen"])

    # Character data (Quotes, Character Arc, and Analysis)
    character_data = {
        "Offred": {
            "quotes": [
                "“I feel like the word shatter is a lovely word for the things that we don’t want to see.”",
                "“Ignoring isn’t the same as ignorance, you have to work at it.”"
            ],
            "arc": "Offred begins as a submissive Handmaid under Gilead’s regime but gradually finds ways to subvert and resist the system, seeking autonomy and self-expression."
        },
        "The Commander": {
            "quotes": [
                "“You can’t make an omelet without breaking eggs.”",
                "“It’s the price we pay for our sins.”"
            ],
            "arc": "The Commander is a high-ranking officer in Gilead, playing a part in maintaining the regime while secretly engaging in activities that contradict the oppressive system he represents."
        },
        "Serina Joy": {
            "quotes": [
                "“A rat in a maze is free to go anywhere, as long as it stays inside the maze.”",
                "“We’re all human, after all.”"
            ],
            "arc": "Serina Joy, initially a powerful figure in the regime, slowly becomes disillusioned with Gilead and grows conflicted about her role in the system."
        },
        "Moira": {
            "quotes": [
                "“Moira was a terrorist. She was a rebel.”",
                "“Don’t let the bastards grind you down.”"
            ],
            "arc": "Moira represents defiance and rebellion against Gilead. Her resistance, while ultimately thwarted, symbolizes hope and the potential for change."
        },
        "Ofglen": {
            "quotes": [
                "“Nolite te bastardes carborundorum.”",
                "“She’s like me. She’s a rebel.”"
            ],
            "arc": "Ofglen represents resistance and underground rebellion within Gilead, being a symbol of hope and strength for Offred."
        }
    }

    # Display selected character's data
    st.write(f"**Key Quotes**:")
    for quote in character_data[character]["quotes"]:
        st.markdown(f"> *{quote}*")

    st.write(f"**Character Arc:**")
    st.write(character_data[character]["arc"])

# --- Character Web ---
elif page == "Character Web":
    st.subheader("🌐 Character Web in The Handmaid's Tale")

    # Example character interaction data (replace with actual data)
    interactions = [
        ("Chapter 1", ["Offred", "The Commander"]),
        ("Chapter 2", ["Offred", "Serina Joy"]),
        ("Chapter 3", ["Offred", "Moira"]),
        ("Chapter 4", ["Offred", "Ofglen"]),
        ("Chapter 5", ["Offred", "The Commander", "Serina Joy"]),
    ]

    # Create a NetworkX graph
    G = nx.Graph()

    # Add interactions as edges between characters
    for chapter, characters in interactions:
        for i in range(len(characters)):
            for j in range(i+1, len(characters)):
                G.add_edge(characters[i], characters[j])

    # Get positions for nodes
    pos = nx.spring_layout(G, seed=42)

    # Extract node and edge data for Plotly visualization
    edges = list(G.edges())
    edge_x = []
    edge_y = []
    for edge in edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_y.append(y0)
        edge_x.append(x1)
        edge_y.append(y1)

    # Nodes
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    # Plotly graph
    fig = go.Figure()

    # Add edges to the figure
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=1, color='#888')))

    # Add nodes to the figure
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers', hoverinfo='text', 
                             marker=dict(size=20, color='skyblue', line=dict(width=2, color='black'))))

    # Add labels (characters' names) to the nodes
    for node in G.nodes():
        fig.add_trace(go.Scatter(x=[pos[node][0]], y=[pos[node][1]], text=[node],
                                 mode='text', textposition="bottom center", showlegend=False))

    # Update the layout of the figure
    fig.update_layout(
        title="Character Relationships in The Handmaid's Tale",
        title_x=0.5,
        showlegend=False,
        height=700,
        width=700,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    )

    # Show the plot
    st.plotly_chart(fig)
