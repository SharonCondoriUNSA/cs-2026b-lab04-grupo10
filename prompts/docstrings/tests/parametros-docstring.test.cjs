const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = path.resolve(__dirname, '..');
const casos = [[], [], [], ['reciclador_id'], ['fecha_recojo'], ['peso_real_kg'],
  ['solicitud_id', 'material', 'peso_real_kg'], ['peso_real_kg']];

for (const version of ['v1', 'v2', 'v3']) {
  const texto = fs.readFileSync(path.join(base, `promptfooconfig-${version}.yaml`), 'utf8');
  const bloque = texto.match(/metric: A2_parametros_exactos_sin_self\r?\n\s+value: \|\r?\n((?: {8}[^\r\n]*(?:\r?\n|$))+)/);
  assert.ok(bloque, `Falta A2 en ${version}`);
  const evaluar = new Function('output', 'context', bloque[1].replace(/^ {8}/gm, ''));
  const leer = id => JSON.parse(fs.readFileSync(path.join(base, 'grabaciones', 'v3', `${id}.txt`), 'utf8'));
  const ejecutar = (respuesta, parametros) => evaluar(JSON.stringify(respuesta),
    { vars: { parametros_esperados: parametros.join(',') } });

  test(`${version}: acepta las ocho respuestas originales con sus firmas`, () => {
    casos.forEach((parametros, i) => assert.equal(ejecutar(leer(`D${i + 1}`), parametros), true));
  });

  test(`${version}: rechaza JSON correcto con argumento inventado solo en docstring`, () => {
    const respuesta = leer('D4');
    respuesta.docstring = `${respuesta.resumen}\n\nArgs:\n    parametro_inexistente: Dato inventado.`;
    assert.equal(ejecutar(respuesta, ['reciclador_id']), false);
  });

  test(`${version}: rechaza omision, duplicacion, self y orden incorrecto`, () => {
    for (const nombres of [[], ['reciclador_id', 'reciclador_id'], ['self', 'reciclador_id']]) {
      const respuesta = leer('D4');
      respuesta.docstring = respuesta.resumen + (nombres.length
        ? '\n\nArgs:\n' + nombres.map(n => `    ${n}: Descripcion valida.`).join('\n') : '');
      assert.equal(ejecutar(respuesta, ['reciclador_id']), false);
    }
    const respuesta = leer('D7');
    respuesta.docstring = respuesta.resumen + '\n\nArgs:\n    material: Material.\n    solicitud_id: Identificador.\n    peso_real_kg: Peso.';
    assert.equal(ejecutar(respuesta, casos[6]), false);
  });

  test(`${version}: rechaza Args inventado en un metodo sin parametros`, () => {
    const respuesta = leer('D1');
    respuesta.docstring += '\n\nArgs:\n    self: Instancia.';
    assert.equal(ejecutar(respuesta, []), false);
  });

  test(`${version}: admite tipos y descripciones continuadas en estilo Args`, () => {
    const respuesta = leer('D4');
    respuesta.docstring = `${respuesta.resumen}\n\nArgs:\n    reciclador_id (UUID): Identificador\n        del reciclador asignado.\n\nRaises:\n    ValueError: Asignacion invalida.`;
    assert.equal(ejecutar(respuesta, ['reciclador_id']), true);
    respuesta.docstring = `${respuesta.resumen}\n\nArgs:\n    reciclador_id:\n        Identificador del reciclador.`;
    assert.equal(ejecutar(respuesta, ['reciclador_id']), true);
  });

  test(`${version}: rechaza secciones duplicadas y descripciones vacias`, () => {
    const respuesta = leer('D4');
    respuesta.docstring += '\n\nArgs:\n    reciclador_id: Duplicado.';
    assert.equal(ejecutar(respuesta, ['reciclador_id']), false);
    respuesta.docstring = `${respuesta.resumen}\n\nArgs:\n    reciclador_id:`;
    assert.equal(ejecutar(respuesta, ['reciclador_id']), false);
  });

  test(`${version}: rechaza parametros distintos en JSON y respuestas malformadas`, () => {
    const respuesta = leer('D4');
    respuesta.parametros[0].nombre = 'otro';
    assert.equal(ejecutar(respuesta, ['reciclador_id']), false);
    for (const output of ['no JSON', 'null', '[]', '{}']) {
      assert.equal(evaluar(output, { vars: { parametros_esperados: 'reciclador_id' } }), false);
    }
  });
}
