# Procedencia de los archivos del revisor

Los 14 archivos de esta tabla proceden de la rama `auditoria/economica-f1-frente-e-revision`, commit `47551a2e76791445f2515311c40d45de6e36cb1b` (padre `96a69ca10cbfd38bea9e6c54a9ef79b9a2eeea0d`), y se copiaron sin cambios con `git cat-file blob`.

| Ruta (relativa a revision/) | Id de blob de git | SHA-256 | Bytes |
|---|---|---|---|
| `REVISION_INDEPENDIENTE_1.md` | `777aed5a18207b77c3561248c48cd03020a69dab` | `7269d5e6ecf9001171bf32880547b97ffbfa46d2051b9b90c41e559b338792b8` | 38503 |
| `resultados_revisor/comprobacion_columnas.txt` | `6010ff1af29052cf3945557622e726a07c03b55f` | `7807ff79b04e5b305c4f6be42a7c9e240790aede3d6a515c42f7d3de34863505` | 1549 |
| `resultados_revisor/prueba_mutantes.txt` | `c65a823f39a285b05b1662ae3205810e036b6e07` | `3b3a85ed524c079bd664e43c1f051a5569885cdb29cb1f9dd38f7c1f97e71701` | 1841 |
| `resultados_revisor/recalculo_independiente.txt` | `0568da036d8b25ab97f01e36210116f44831ba37` | `aef25d88f8ce7c1b290ae30d1c05d49ed1be782ee1b6dc3515395036d2479ac2` | 4458 |
| `resultados_revisor/replica_motor_A.txt` | `d834cecc27a9d0249725a09073e19000a051bae0` | `7d0bfb813ab6f61ee04abaf8f6d0611d8b3378bd27982cebd2eb1a7d670e8e83` | 525 |
| `resultados_revisor/sensibilidades_revision.txt` | `fdda03d933015faff86103905490fb37a7bb0592` | `6962c79fda812bc83e6d10cc2c4c11288527902a67e808991d2cc01ed7c6bf94` | 2033 |
| `scripts_revisor/busca.py` | `646840ddf94402c657235b79078beef6cb8d15a2` | `eea65ed8150477f958ca3581599ca2b93c89eac5e86d26ff6731399f63b3b4a1` | 646 |
| `scripts_revisor/comprobacion_columnas.py` | `e02092eaf87fe04edfd981b86692bd05629a3408` | `750dd01c29fc2bd3ed7bcfa2551e781270c5b2a0042a93b3d257c0946ac5279b` | 4116 |
| `scripts_revisor/libro_dump.py` | `ffd992cc87723540f70bbb7673677788f2557ef9` | `897889d7b4e6dbf443cf1ae1940bd29a50f6b5d3500aae6ec3d5215c4c1e604a` | 1062 |
| `scripts_revisor/pag.py` | `7c48460b078fcd0b74139183045e9a0e31c8fb05` | `2f14d903703939ec79298322cab7e77ce7a9df0335c519687ba43503b3289deb` | 763 |
| `scripts_revisor/prueba_mutantes.py` | `f9c8e8c9590ab56d085b99560b0ffba62ead880a` | `d0155b2caf641f743ad53b6663e626d5d2e61be8b66931a4d598fe0439289ba9` | 5154 |
| `scripts_revisor/recalculo_independiente.py` | `51872230f5d230ec50604e17d04290abb73c12a1` | `1bcf58674005f17af9c499766ad79b014ed6c73e9a775cd470f704a23ecb2440` | 10517 |
| `scripts_revisor/replica_motor_A.py` | `c8082ca47c80de5bfd8d63d0b9094d83c63a60d9` | `768bb167e7b2f41f28d3f961590cb1f74e35bad72347c64450a44bb3fd2f296a` | 1906 |
| `scripts_revisor/sensibilidades_revision.py` | `3937d89dd00b0d6e4758d51e1c3ad8127f22bc6c` | `4a8d7c9f5203c06c1107636b206b5f5883972e8694f65a21f22d711f9aed2754` | 4546 |

Comprobación (desde la raíz del repositorio): `git diff --name-only 96a69ca 47551a2e76791445f2515311c40d45de6e36cb1b | while read p; do [ "$(git hash-object "$p")" = "$(git ls-tree 47551a2e76791445f2515311c40d45de6e36cb1b "$p" | awk '{print $3}')" ] && echo "OK $p" || echo "DISTINTO $p"; done`
