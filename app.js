const fs = require("fs");
const readline = require("readline");

function lerJson(caminho) {
  try {
    const conteudo = fs.readFileSync(caminho, "utf8").replace(/^\uFEFF/, "");
    return JSON.parse(conteudo);
  } catch (erro) {
    console.log(`erro ao ler ${caminho}: ${erro.message}`);
    process.exit(1);
  }
}

function normalizarTexto(texto) {
  return String(texto)
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\s+/g, " ");
}

const municipios = lerJson("municipios.json");
const estados = lerJson("estados.json");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question("digite o municipio: ", (nomeMunicipioInput) => {
  rl.question("digite a UF: ", async (ufInput) => {
    const nome_municipio = normalizarTexto(nomeMunicipioInput);
    const uf_digitada = ufInput.trim().toUpperCase();

    let codigo_uf = null;

    for (const estado of estados) {
      if (String(estado.uf).toUpperCase() === uf_digitada) {
        codigo_uf = estado.codigo_uf;
        break;
      }
    }

    if (codigo_uf === null) {
      console.log("UF n encontrada");
      rl.close();
      return;
    }

    let municipio_encontrado = null;

    for (const municipio of municipios) {
      if (
        normalizarTexto(municipio.nome) === nome_municipio &&
        Number(municipio.codigo_uf) === Number(codigo_uf)
      ) {
        municipio_encontrado = municipio;
        break;
      }
    }

    if (!municipio_encontrado) {
      console.log("municio não encontrado nessa UF");
      rl.close();
      return;
    }

    const lat = municipio_encontrado.latitude;
    const lon = municipio_encontrado.longitude;

    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m&timezone=auto`;

    try {
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`status ${response.status}`);
      }

      const data = await response.json();
      const temperatura = data.current.temperature_2m;

      console.log(`\nmunicipio: ${municipio_encontrado.nome} - ${uf_digitada}`);
      console.log(`lat: ${lat}`);
      console.log(`lon: ${lon}`);
      console.log(`temp atual: ${temperatura} C`);
    } catch (e) {
      console.log(`Erro ao consultar a API: ${e.message}`);
    }

    rl.close();
  });
});