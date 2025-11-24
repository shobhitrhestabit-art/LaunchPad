const LOG_KEY = "error_logs";

export function addErrorLog(message, extras = {}) {
    const logs = JSON.parse(localStorage.getItem(LOG_KEY)) || [];
    logs.push({
        time: new Date().toISOString(),
        message,
        ...extras
    });
    localStorage.setItem(LOG_KEY, JSON.stringify(logs));
}
