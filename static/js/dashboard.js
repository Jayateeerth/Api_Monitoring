
const tableBody = document.getElementById("logs-table-body");
const totalRequests = document.getElementById("total-requests");
const successfulRequests = document.getElementById("successful-requests");
const failedRequests = document.getElementById("failed-requests");
const averageDuration = document.getElementById("average-duration");
const logCount = document.getElementById("log-count");
const refreshButton = document.getElementById("refresh-button");

const searchInput = document.getElementById("search-input");
const statusFilter = document.getElementById("status-filter");
const methodFilter = document.getElementById("method-filter");

let allLogs = [];

function getStatusClass(status) {
    if (status >= 500) return "error";
    if (status >= 400) return "warning";
    return "success";
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);

    return Number.isNaN(date.getTime())
        ? (timestamp ?? "—")
        : date.toLocaleString();
}

function renderLogs(logs) {
    tableBody.replaceChildren();

    if (!logs.length) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 5;
        cell.className = "empty-state";
        cell.textContent = "No matching request logs found.";

        row.appendChild(cell);
        tableBody.appendChild(row);
        return;
    }

    for (const log of logs) {
        const row = document.createElement("tr");

        const methodCell = document.createElement("td");
        methodCell.className = "method";
        methodCell.textContent = log.method ?? "—";

        const endpointCell = document.createElement("td");
        endpointCell.className = "endpoint";
        endpointCell.textContent = log.endpoint ?? "—";

        const statusCell = document.createElement("td");
        const badge = document.createElement("span");

        badge.className = `status ${getStatusClass(log.status_code)}`;
        badge.textContent = log.status_code ?? "—";
        statusCell.appendChild(badge);

        const durationCell = document.createElement("td");
        durationCell.className = "duration";
        durationCell.textContent =
            `${Number(log.duration_ms).toFixed(2)} ms`;

        const timestampCell = document.createElement("td");
        timestampCell.className = "timestamp";
        timestampCell.textContent = formatTimestamp(log.timestamp);

        row.append(
            methodCell,
            endpointCell,
            statusCell,
            durationCell,
            timestampCell
        );

        tableBody.appendChild(row);
    }
}

function applyFilters() {
    const search = searchInput.value.trim().toLowerCase();
    const selectedStatus = statusFilter.value;
    const selectedMethod = methodFilter.value;

    const filteredLogs = allLogs.filter(log => {
        const matchesSearch =
            (log.endpoint ?? "").toLowerCase().includes(search);

        const matchesMethod =
            !selectedMethod || log.method === selectedMethod;

        const matchesStatus =
            !selectedStatus ||
            String(log.status_code).startsWith(selectedStatus);

        return matchesSearch && matchesMethod && matchesStatus;
    });

    const successful = filteredLogs.filter(
        log => log.status_code >= 200 && log.status_code < 300
    );

    const failed = filteredLogs.filter(
        log => log.status_code >= 400
    );

    const average = filteredLogs.length
        ? filteredLogs.reduce(
            (sum, log) => sum + Number(log.duration_ms), 0
        ) / filteredLogs.length
        : 0;

    totalRequests.textContent = filteredLogs.length;
    successfulRequests.textContent = successful.length;
    failedRequests.textContent = failed.length;
    averageDuration.textContent = `${average.toFixed(2)} ms`;

    renderLogs(filteredLogs);

    logCount.textContent =
        `${filteredLogs.length} of ${allLogs.length} loaded requests`;
}

async function loadLogs() {
    refreshButton.disabled = true;
    refreshButton.textContent = "Loading...";

    try {
        const response = await fetch("/api/logs?limit=100");

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        allLogs = data.logs ?? [];

        applyFilters();
    } catch (error) {
        console.error("Unable to load logs:", error);
        logCount.textContent = "Failed to load logs";
    } finally {
        refreshButton.disabled = false;
        refreshButton.textContent = "↻ Refresh";
    }
}

searchInput.addEventListener("input", applyFilters);
statusFilter.addEventListener("change", applyFilters);
methodFilter.addEventListener("change", applyFilters);
refreshButton.addEventListener("click", loadLogs);

loadLogs();

// Refresh the displayed data every 10 seconds.
setInterval(loadLogs, 10000);
