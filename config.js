const CONFIG = {
    // Estas configuraciones ahora se manejan idealmente vía variables de entorno en Vercel.
    // NOTEBOOK_NAME y HANDLES se mantienen para referencia en el frontend.
    NOTEBOOK_NAME: 'IA Tools 2',
    HANDLES: [
        "@GoogleCloudTech", "@googlecloud", "@geminicli", "@ChromiumDev",
        "@antigravity", "@julesagent", "@GoogleResearch", "@n8n_io",
        "@GoogleDesign", "@GoogleAIStudio"
    ],
    API_ENDPOINTS: {
        CHAT: '/api/chat',
        HARVEST: '/api/harvest',
        TECH: '/api/tech'
    }
};

export default CONFIG;
