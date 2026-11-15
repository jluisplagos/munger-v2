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

## Revisión independiente n.º 3 y su adenda

Los 16 archivos de esta tabla proceden de la rama `auditoria/economica-f1-frente-e-revision`. El informe principal está en el commit `11b999a74bc1803e9273b185d3581115258b0923` (padre `47551a2e76791445f2515311c40d45de6e36cb1b`) y la adenda en el commit `034301cae8e2f1a21107b017d18eb67075ec5d33` (hijo de `11b999a74bc1803e9273b185d3581115258b0923`). Se copiaron las versiones de `034301cae8e2f1a21107b017d18eb67075ec5d33` sin cambios con `git cat-file blob`.

| Ruta (relativa a revision/) | Commit del último cambio | Id de blob de git | SHA-256 | Bytes |
|---|---|---|---|---|
| `REVISION_INDEPENDIENTE_3.md` | `034301c` | `792845bb81628561906a393e966b617b47d5209b` | `92237bcc90911f70c57001344cd1a1cdd1d3ae6b04cfdc88875a2add4d32581d` | 56492 |
| `resultados_revisor_3/cobertura_por_mutacion.txt` | `11b999a` | `327ebc7f865e6ca255d2feca375473d647987489` | `1dab48f2d6e3d1b57241995f13c08b8ccfd878a40dddb2adf303eb9316b677a4` | 22394 |
| `resultados_revisor_3/comprobacion_tokens.txt` | `11b999a` | `9cdc59218d96d5ee9868eef7f0022db23ab2bef6` | `67858842bb96137034c20784ac2d8cf195d4a20672a18c1433c0c6e5eaaa7a16` | 187 |
| `resultados_revisor_3/prueba_mutantes_3.txt` | `11b999a` | `457dc30ffe1de43f93fa9164ee116d286e6682dc` | `db50dcf5fac7f2a642a1061c4584939fbbbfce3634bd87c85852a4312e8f6327` | 7351 |
| `resultados_revisor_3/prueba_mutantes_3_sobre_f30c66c.txt` | `034301c` | `457dc30ffe1de43f93fa9164ee116d286e6682dc` | `db50dcf5fac7f2a642a1061c4584939fbbbfce3634bd87c85852a4312e8f6327` | 7351 |
| `resultados_revisor_3/prueba_mutantes_3b.txt` | `11b999a` | `b95ed89ab46e53abb1d2b92133c97ec7cbdb8ca2` | `7d57dd2b8a5be8a411945149786c83fc67d41a22dda2099c63e35e36ef837bf6` | 4089 |
| `resultados_revisor_3/prueba_mutantes_3b_sobre_f30c66c.txt` | `034301c` | `b95ed89ab46e53abb1d2b92133c97ec7cbdb8ca2` | `7d57dd2b8a5be8a411945149786c83fc67d41a22dda2099c63e35e36ef837bf6` | 4089 |
| `resultados_revisor_3/prueba_mutantes_rev1_sobre_commit_congelado.txt` | `11b999a` | `3038687c42c2daef31518b2c06bbc48a3064b23f` | `ef1b57cd713fdd9bd97bc7aacb26b7006a76d6258e3de2ebd3459f42b66f8e0b` | 1389 |
| `resultados_revisor_3/recalculo_3.txt` | `11b999a` | `68cdc50927a984d769cd4f7d6a65f146cc4c4aa9` | `7ce920a6d9463b473e457e020d63f89d2c1616ca34f13f811eb2cc2b68478013` | 6641 |
| `resultados_revisor_3/sondas_revisor.txt` | `034301c` | `c6007069e96c8eb8d204829ccf6b55f60b07aad6` | `c4115cb89174e826fead17abec1d68494e602a80306f3bb6a7a6a04dee9e0c10` | 10513 |
| `scripts_revisor_3/cobertura_por_mutacion.py` | `11b999a` | `6799169d9ec82e97977e26d938f54e8643455f5b` | `df72a29db78ffbdbca885a79048aa0287de3480ba28140de21c897dc705878f2` | 5828 |
| `scripts_revisor_3/comprobacion_tokens.py` | `11b999a` | `94f5880eb20a18ce2e802a7b1afe257e8c9593e1` | `b764202fc97298c2ef03b83f9e73ea1ddeb82b9f12882224bfc91bffe51336f1` | 2373 |
| `scripts_revisor_3/prueba_mutantes_3.py` | `11b999a` | `0f3fabb1f2549f2449121bab180c571ca70bb44c` | `f3a4764b63129562e38e22f5094273e382d337cf77fad15aeddea118b84362c1` | 8480 |
| `scripts_revisor_3/prueba_mutantes_3b.py` | `11b999a` | `9e4aa025a8bc89b35a178acc95f7114333e910ad` | `67fcd260110f24c12e53ebb76dc5f89997ab884812763b9bc0b356fc2509d318` | 7710 |
| `scripts_revisor_3/recalculo_3.py` | `11b999a` | `620bb9a0657298d52fa61fe7a8cf71d00f2101a9` | `27501fac1fed2e14d16c8dee216ca1e86f2a5b895642b6305783e81c68aca616` | 10723 |
| `scripts_revisor_3/sondas_revisor.py` | `034301c` | `0aa747658d9d5a48fd6f48266f6a7bb5384d38c2` | `1c99b5126107c9a8cc860715c7fde91e2ed4ade107e4fe1e42aaa27ebdafc087` | 11784 |

Comprobación (desde la raíz del repositorio): `git diff --name-only 47551a2e76791445f2515311c40d45de6e36cb1b 034301cae8e2f1a21107b017d18eb67075ec5d33 | while read p; do [ "$(git hash-object "$p")" = "$(git ls-tree 034301cae8e2f1a21107b017d18eb67075ec5d33 "$p" | awk '{print $3}')" ] && echo "OK $p" || echo "DISTINTO $p"; done`

## Revisión independiente n.º 4

Los 5 archivos de esta tabla proceden de la rama `auditoria/economica-f1-frente-e-revision`, commit `a15f70632ed1850f0d68ccfcfaf1c146a43d1796` (padre `034301cae8e2f1a21107b017d18eb67075ec5d33`), publicado el 15 de noviembre de 2026 a las 22:04:29 UTC, y se copiaron sin cambios en las mismas rutas con `git show`.

| Ruta (relativa a revision/) | Commit del último cambio | Id de blob de git | SHA-256 | Bytes |
|---|---|---|---|---|
| `REVISION_INDEPENDIENTE_4.md` | `a15f706` | `489d486a9e028daa02d3ae0af2e905e62fcc3e88` | `020ffb9ef7d392ef7584a7fd382b57e80fdaf92fe33d862fc55be9ac2923923e` | 22123 |
| `resultados_revisor_4/contraejemplos_4.txt` | `a15f706` | `d3918ed71713924084fec8a82ffb7cc66a865e59` | `77c50b456db5ea2b3fda87cf127460c4ecdbe41cef5452102e11b4e56763dda5` | 6259 |
| `resultados_revisor_4/paginas_sin_ancla.txt` | `a15f706` | `fa2eb5d6867c05c7135b512b9671b4c4af4c5665` | `1e3df56684fd11e8387d60bcba17ce900344b7333821266b9ee69c7964f349ae` | 2235 |
| `scripts_revisor_4/contraejemplos_4.py` | `a15f706` | `91f6391056afec9ae0e144f0f9545bd00592c449` | `31680ca42a189797c6d152d4f9ae97ef6abf74a29a0dbc6bd4bb5f967ca734e0` | 11503 |
| `scripts_revisor_4/paginas_sin_ancla.py` | `a15f706` | `7d63f7e18230733ba0d5f7c8d6b35c51d51cc682` | `d96b9ce166457dfcda420fcb6bfe29156ff5dca73812b7c77e91caac162d228a` | 2000 |

Comprobación (desde la raíz del repositorio): `git diff --name-only 034301cae8e2f1a21107b017d18eb67075ec5d33 a15f70632ed1850f0d68ccfcfaf1c146a43d1796 | while read p; do [ "$(git hash-object "$p")" = "$(git ls-tree a15f70632ed1850f0d68ccfcfaf1c146a43d1796 "$p" | awk '{print $3}')" ] && echo "OK $p" || echo "DISTINTO $p"; done`
