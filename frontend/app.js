window.onload = () => {
    loadItems();
    loadCategories();
};

async function loadCategories() {
    const res = await fetch('http://127.0.0.1:8000/categories');
    const cats = await res.json();
    document.getElementById('itemCat').innerHTML =
        cats.map(c => `<option value="${c}">${c}</option>`).join('');
}

async function addCategory() {
    const newCat = prompt("Enter new category:");
    if (!newCat) return;

    await fetch('http://127.0.0.1:8000/categories', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({category: newCat})
    });

    loadCategories();
}

async function loadItems() {
    const res = await fetch('http://127.0.0.1:8000/items');
    const items = await res.json();
    renderTable(items);
}

function renderTable(items) {
    const table = document.getElementById('inventoryTable');

    table.innerHTML = items.map(i => `
        <tr class="border-b border-gray-700">
            <td class="p-4">#${i.id.toString().slice(-4)}</td>
            <td class="p-4">${i.name}</td>
            <td class="p-4">${i.qty} ${i.unit}</td>
            <td class="p-4">${i.category}</td>
            <td class="p-4 text-right space-x-3">
                <button onclick="consumeItem(${i.id})" class="text-orange-400">Consume</button>
                <button onclick="updateItem(${i.id})" class="text-blue-400">Update</button>
                <button onclick="deleteItem(${i.id})" class="text-red-400">Delete</button>
            </td>
        </tr>
    `).join('');
}

async function saveItem() {
    const item = {
        id: 0,
        name: document.getElementById('itemName').value,
        qty: parseInt(document.getElementById('itemQty').value),
        unit: document.getElementById('itemUnit').value,
        category: document.getElementById('itemCat').value
    };

    await fetch('http://127.0.0.1:8000/items', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(item)
    });

    loadItems();
}

async function consumeItem(id) {
    const amount = prompt("Enter quantity to consume:");
    if (!amount) return;

    await fetch(`http://127.0.0.1:8000/items/consume/${id}?amount=${amount}`, {
        method: 'POST'
    });

    loadItems();
}

async function updateItem(id) {
    const newQty = prompt("Enter new quantity:");
    if (!newQty) return;

    await fetch(`http://127.0.0.1:8000/items/update/${id}?qty=${newQty}`, {
        method: 'PUT'
    });

    loadItems();
}

async function deleteItem(id) {
    if (!confirm("Are you sure?")) return;

    await fetch(`http://127.0.0.1:8000/items/${id}`, {
        method: 'DELETE'
    });

    loadItems();
}

async function recoverItem() {
    const id = prompt("Enter Item ID to recover:");
    if (!id) return;

    await fetch(`http://127.0.0.1:8000/items/recover/${id}`, {
        method: 'POST'
    });

    loadItems();
}

async function showHistory() {
    const res = await fetch('http://127.0.0.1:8000/history');
    const history = await res.json();
    alert(history.map(h => `${h.time}: ${h.msg}`).join('\n'));
}
