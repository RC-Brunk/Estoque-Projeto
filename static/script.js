async function listarProdutos() {
    try {
        const response = await fetch('http://localhost:5000/produtos');
        const produtos = await response.json();
        console.log("Produtos recebidos:", produtos); // Para depuração
        const tbody = document.getElementById('produtosTableBody');
        tbody.innerHTML = '';
        produtos.forEach(produto => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${produto.id}</td>
                <td>${produto.nome}</td>
                <td>${produto.quantidade}</td>
                <td>${produto.categoria}</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editarProduto(${produto.id})">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="excluirProduto(${produto.id})">Excluir</button>
                </td>
            `;
            if (produto.quantidade < 5) {
                row.innerHTML += `<td><span class="text-danger">Estoque baixo!</span></td>`;
            }
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Erro ao listar produtos:', error);
    }
}

document.getElementById('produtoForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const nome = document.getElementById('nome').value;
    const quantidade = parseInt(document.getElementById('quantidade').value);
    const categoria = document.getElementById('categoria').value;
    console.log("Formulário enviado! Dados:", { nome, quantidade, categoria }); // Para depuração

    try {
        const response = await fetch('http://localhost:5000/produtos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, quantidade, categoria }),
        });
        console.log("Resposta do servidor:", response); // Para depuração
        if (response.ok) {
            alert('Produto adicionado com sucesso!');
            listarProdutos();
            document.getElementById('produtoForm').reset();
        } else {
            console.log("Erro na resposta:", await response.text()); // Para depuração
            alert('Erro ao adicionar produto');
        }
    } catch (error) {
        console.error('Erro ao adicionar produto:', error);
    }
});

async function editarProduto(id) {
    const nome = prompt('Novo nome do produto:');
    const quantidade = parseInt(prompt('Nova quantidade:'));
    const categoria = prompt('Nova categoria:');

    if (nome && !isNaN(quantidade) && categoria) {
        try {
            const response = await fetch(`http://localhost:5000/produtos/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nome, quantidade, categoria }),
            });
            if (response.ok) {
                alert('Produto atualizado com sucesso!');
                listarProdutos();
            } else {
                alert('Erro ao atualizar produto');
            }
        } catch (error) {
            console.error('Erro ao atualizar produto:', error);
        }
    } else {
        alert('Preencha todos os campos corretamente!');
    }
}

async function excluirProduto(id) {
    if (confirm('Tem certeza que deseja excluir este produto?')) {
        try {
            const response = await fetch(`http://localhost:5000/produtos/${id}`, {
                method: 'DELETE',
            });
            if (response.ok) {
                alert('Produto excluído com sucesso!');
                listarProdutos();
            } else {
                alert('Erro ao excluir produto');
            }
        } catch (error) {
            console.error('Erro ao excluir produto:', error);
        }
    }
}

window.onload = listarProdutos;