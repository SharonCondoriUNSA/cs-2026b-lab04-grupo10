const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const base = path.resolve(__dirname, '..');
const configuraciones = ['promptfooconfig.yaml', 'promptfooconfig-v2.yaml', 'promptfooconfig-v3.yaml'];

for (const archivo of configuraciones) {
  // Ejecuta el bloque real de A6, sin duplicar su implementación en la prueba.
  const texto = fs.readFileSync(path.join(base, archivo), 'utf8');
  const bloque = texto.match(/metric: A6_historia_id_corresponde_al_caso\r?\n\s+value: \|\r?\n((?: {8}[^\r\n]*(?:\r?\n|$))+)/);
  assert.ok(bloque, `Falta A6 en ${archivo}`);
  const evaluar = new Function('output', 'context', bloque[1].replace(/^ {8}/gm, ''));

  test(`${archivo}: acepta los ocho identificadores originales de v3`, () => {
    for (let i = 1; i <= 8; i++) {
      const id = `H${i}`;
      const salida = fs.readFileSync(path.join(base, 'grabaciones', 'v3', `${id}.txt`), 'utf8');
      assert.equal(evaluar(salida, { vars: { id } }), true, id);
    }
  });

  test(`${archivo}: rechaza ID intercambiado en casos normales, no INVEST y adversarios`, () => {
    for (const id of ['H1', 'H7', 'H8']) {
      const original = JSON.parse(fs.readFileSync(path.join(base, 'grabaciones', 'v3', `${id}.txt`), 'utf8'));
      original.historia_id = 'H99';
      assert.equal(evaluar(JSON.stringify(original), { vars: { id } }), false, id);
    }
  });

  test(`${archivo}: rechaza salidas sin identificador o con tipo incorrecto`, () => {
    for (const salida of ['sin JSON', 'null', '[]', '{}', '"H1"', '{"historia_id":1}']) {
      assert.equal(evaluar(salida, { vars: { id: 'H1' } }), false, salida);
    }
  });

  test(`${archivo}: no acepta un caso sin identificador esperado`, () => {
    for (const contexto of [undefined, {}, { vars: {} }, { vars: { id: '' } }, { vars: { id: 1 } }]) {
      assert.equal(evaluar('{"historia_id":"H1"}', contexto), false);
    }
  });
}
