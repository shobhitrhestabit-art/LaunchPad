export function groupBy(arr, key) {
    return arr.reduce((acc, item) => {
        const k = typeof key === "function" ? key(item) : item[key];
        (acc[k] = acc[k] || []).push(item);
        return acc;
    }, {});
}
