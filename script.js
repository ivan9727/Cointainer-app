(() => {
	const ports = [
		"Ålesund",
		"Stavanger",
		"Haugesund",
		"Molde",
		"Førde",
		"Trondheim",
	];

	const statuses = [
		"empty",
		"B",
		"T",
		"lastcast",
		"module",
		"7pc",
		"ADR",
		"Ikke ADR",
	];

	/** @type {Array<{id:number, date:string, port:string, containerNumber:string, status:string, arrivalTime:string, comment:string, isEditing?:boolean}>} */
	let entries = [];

	const form = document.getElementById("entryForm");
	const dateInput = document.getElementById("date");
	const portSelect = document.getElementById("port");
	const containerInput = document.getElementById("containerNumber");
	const statusSelect = document.getElementById("status");
	const arrivalInput = document.getElementById("arrivalTime");
	const commentInput = document.getElementById("comment");
	const tbody = document.getElementById("entriesTbody");

	function toTodayDateString() {
		const now = new Date();
		const year = now.getFullYear();
		const month = String(now.getMonth() + 1).padStart(2, "0");
		const day = String(now.getDate()).padStart(2, "0");
		return `${year}-${month}-${day}`;
	}

	function setDefaultDateIfEmpty() {
		if (!dateInput.value) {
			dateInput.value = toTodayDateString();
		}
	}

	function clearEntryInputsAfterAdd() {
		containerInput.value = "";
		arrivalInput.value = "";
		commentInput.value = "";
		containerInput.focus();
	}

	function createSelectOptions(options, selected) {
		return options
			.map((opt) => `<option value="${opt.replace(/"/g, '&quot;')}` + `"${opt === selected ? " selected" : ""}>${opt}</option>`) // ensure simple escaping of quotes
			.join("");
	}

	function render() {
		const rows = entries.map((entry) => {
			if (entry.isEditing) {
				return `
				<tr data-id="${entry.id}">
					<td><input type="date" class="input-compact" value="${entry.date}"></td>
					<td>
						<select class="select-compact">${createSelectOptions(ports, entry.port)}</select>
					</td>
					<td><input type="text" class="input-compact" value="${escapeHtml(entry.containerNumber)}"></td>
					<td>
						<select class="select-compact">${createSelectOptions(statuses, entry.status)}</select>
					</td>
					<td><input type="time" class="input-compact" value="${entry.arrivalTime || ""}"></td>
					<td><textarea class="textarea-compact" rows="2">${escapeHtml(entry.comment || "")}</textarea></td>
					<td class="nowrap">
						<button class="action-btn" data-action="save">Save</button>
						<button class="action-btn" data-action="cancel">Cancel</button>
					</td>
				</tr>`;
			}

			return `
			<tr data-id="${entry.id}">
				<td>${entry.date}</td>
				<td>${entry.port}</td>
				<td>${escapeHtml(entry.containerNumber)}</td>
				<td>${entry.status}</td>
				<td>${entry.arrivalTime || ""}</td>
				<td>${escapeHtml(entry.comment || "")}</td>
				<td class="nowrap">
					<button class="action-btn" data-action="edit">Edit</button>
					<button class="action-btn danger" data-action="delete">Delete</button>
				</td>
			</tr>`;
		}).join("");

		tbody.innerHTML = rows || "";
	}

	function escapeHtml(unsafe) {
		return String(unsafe)
			.replace(/&/g, "&amp;")
			.replace(/</g, "&lt;")
			.replace(/>/g, "&gt;")
			.replace(/"/g, "&quot;")
			.replace(/'/g, "&#039;");
	}

	form.addEventListener("submit", (e) => {
		e.preventDefault();
		setDefaultDateIfEmpty();
		const formData = new FormData(form);
		const date = formData.get("date");
		const port = formData.get("port");
		const containerNumber = String(formData.get("containerNumber") || "").trim();
		const status = formData.get("status");
		const arrivalTime = formData.get("arrivalTime") || "";
		const comment = String(formData.get("comment") || "").trim();

		if (!containerNumber) {
			containerInput.focus();
			return;
		}

		entries.unshift({
			id: Date.now() + Math.floor(Math.random() * 1000),
			date: String(date),
			port: String(port),
			containerNumber,
			status: String(status),
			arrivalTime: String(arrivalTime),
			comment,
		});

		render();
		clearEntryInputsAfterAdd();
	});

	tbody.addEventListener("click", (e) => {
		const target = /** @type {HTMLElement} */(e.target);
		const action = target.getAttribute("data-action");
		if (!action) return;

		const row = target.closest("tr");
		if (!row) return;
		const id = Number(row.getAttribute("data-id"));
		const idx = entries.findIndex((x) => x.id === id);
		if (idx === -1) return;

		if (action === "edit") {
			entries = entries.map((x) => ({ ...x, isEditing: x.id === id }));
			render();
			return;
		}

		if (action === "cancel") {
			entries[idx].isEditing = false;
			render();
			return;
		}

		if (action === "save") {
			const inputs = row.querySelectorAll("input, select, textarea");
			const [dateEl, portEl, containerEl, statusEl, timeEl, commentEl] = inputs;
			const newDate = /** @type {HTMLInputElement} */(dateEl).value || toTodayDateString();
			const newPort = /** @type {HTMLSelectElement} */(portEl).value;
			const newContainer = (/** @type {HTMLInputElement} */(containerEl).value || "").trim();
			const newStatus = /** @type {HTMLSelectElement} */(statusEl).value;
			const newTime = /** @type {HTMLInputElement} */(timeEl).value;
			const newComment = (/** @type {HTMLTextAreaElement} */(commentEl).value || "").trim();

			if (!newContainer) {
				/** @type {HTMLInputElement} */(containerEl).focus();
				return;
			}

			entries[idx] = {
				...entries[idx],
				date: newDate,
				port: newPort,
				containerNumber: newContainer,
				status: newStatus,
				arrivalTime: newTime,
				comment: newComment,
				isEditing: false,
			};

			render();
			return;
		}

		if (action === "delete") {
			entries.splice(idx, 1);
			render();
			return;
		}
	});

	// Initialize defaults
	document.addEventListener("DOMContentLoaded", () => {
		setDefaultDateIfEmpty();
	});

	// Ensure default date on first load without waiting for DOMContentLoaded in modern browsers
	setDefaultDateIfEmpty();
	render();
})();

