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

## Revisión independiente n.º 5

Los 12 archivos de esta tabla proceden de la rama `auditoria/economica-f1-frente-e-revision`, commit `595d2f678178e41dac15e8d24b0523efe327b5b8` (padre `a15f70632ed1850f0d68ccfcfaf1c146a43d1796`), publicado el 15 de noviembre de 2026 a las 23:19:11 UTC por una sesión de revisión nueva, distinta de la de las revisiones n.º 1, 3 y 4, y se copiaron sin cambios en las mismas rutas con `git show`.

| Ruta (relativa a revision/) | Commit del último cambio | Id de blob de git | SHA-256 | Bytes |
|---|---|---|---|---|
| `REVISION_INDEPENDIENTE_5.md` | `595d2f6` | `3709a3cbe1131196e6c0bf57020599dffb5cae53` | `9fe5623d9534047ac3044a1d2f3b1eeb45cd06fba02b1e9e49db342640dd0c8c` | 38011 |
| `resultados_revisor_5/barrido_tablas.txt` | `595d2f6` | `09788eb1cee7f35494b122796d358516524c23b7` | `3029e719e4dedd1692bf5d20e6ed716de0d8c0e7aa2f24b54268c4a46065f51c` | 70216 |
| `resultados_revisor_5/clases_5.txt` | `595d2f6` | `e0803e980f98542e4a7a888623ac8ba405006c88` | `20088490f7ecee391a28b7ba0375611a2557abe2b32a6623d57d101e01217b9e` | 5605 |
| `resultados_revisor_5/cobertura_propia.txt` | `595d2f6` | `e98c20f79f2528650608b7ee3d5a62e73d8be4de` | `a8fa2406735f107ee6b9b61a501ebe5df0557cdb2be37731f24e345f0b34b815` | 3943 |
| `resultados_revisor_5/contraejemplos_5.txt` | `595d2f6` | `2e1b080fe8444245b7dc61b2445b9e496892e22a` | `f34a685a1a25adbf33260a2766cec01375206745a8f6eba872a48137188b726f` | 31435 |
| `resultados_revisor_5/lectura_filas_c9.txt` | `595d2f6` | `90e0fbf9659b48aa777061de05b786f875b1899e` | `0c391defa24d007a3d439323e9f711ccf0216001502e3747a1862963d72d866f` | 18078 |
| `scripts_revisor_5/arnes.py` | `595d2f6` | `aedbce3c878f1ac19aca241115be567d92cb292d` | `52e17cc7aac114072acc9ad35890021a336bcc2cdfe7451a2f61dee8c1ec635b` | 5303 |
| `scripts_revisor_5/barrido_tablas.py` | `595d2f6` | `ae929fbd9c147364b46a96ce82a947f7db488821` | `68d987a1d48c889bbb99577bd240cd7a7fccf6ba5a649a8dc2037f6a2c38acf3` | 17324 |
| `scripts_revisor_5/clases_5.py` | `595d2f6` | `c700525857e9130adb78e198b03c02a1b2d9d79b` | `5dbd6b44042e082d0e0d64ba964c49a986af02281bdac637681b3c1da36b4b31` | 13902 |
| `scripts_revisor_5/cobertura_propia.py` | `595d2f6` | `2768503376301e731bc168fd55c432fc1c6aa565` | `ab1e99304204af6308b306ccec39bf49389cf8b9c7bb76ffc1c0e02e11bbe308` | 12856 |
| `scripts_revisor_5/contraejemplos_5.py` | `595d2f6` | `78fafc2967b387b2b0dbd536a2117ac6523ae186` | `da3171982dcef742e4a9af1af88b8a8045759967f46a2b106eaeed00bcd13255` | 14976 |
| `scripts_revisor_5/lectura_filas_c9.py` | `595d2f6` | `1484b5c6c1872781653c19af5f6f27bb911ecdcb` | `39cae31c978dab45a0e693afeda434e389e4f957e3e0c7870435c4ae243ed0b4` | 15018 |

Comprobación (desde la raíz del repositorio): `git diff --name-only a15f70632ed1850f0d68ccfcfaf1c146a43d1796 595d2f678178e41dac15e8d24b0523efe327b5b8 | while read p; do [ "$(git hash-object "$p")" = "$(git ls-tree 595d2f678178e41dac15e8d24b0523efe327b5b8 "$p" | awk '{print $3}')" ] && echo "OK $p" || echo "DISTINTO $p"; done`

## Revisión independiente n.º 6

Los 16 archivos de esta tabla proceden de la rama `auditoria/economica-f1-frente-e-revision`, commit `9711f04eba236c31100d0e3bd631b276c804e8c4` (padre `595d2f678178e41dac15e8d24b0523efe327b5b8`), publicado el 16 de noviembre de 2026 a las 01:24:49 UTC por una sesión de revisión nueva, distinta de las de las revisiones n.º 1, 3, 4 y 5, y se copiaron sin cambios en las mismas rutas con `git show`.

| Ruta (relativa a revision/) | Commit del último cambio | Id de blob de git | SHA-256 | Bytes |
|---|---|---|---|---|
| `REVISION_INDEPENDIENTE_6.md` | `9711f04` | `efc13cfb37467b61e7cdad14a55fe9c36b9f3d72` | `8ddc2adcebde337bdbbe4aef54aa8770cee1132c680dab1aeaa2f58271aee2d8` | 50975 |
| `resultados_revisor_6/barrido_6.txt` | `9711f04` | `8ae7bd84d32232b485aee3d6f425a6239069afe7` | `d00e00e02e92cd8450a8d02820193e895b62c68e204615622882fddb9abb3b87` | 13159 |
| `resultados_revisor_6/clases_6.txt` | `9711f04` | `c035f82febce1a8644d1d2710457ebb3e358fc24` | `4e6afc3532de5416a2926588e1c0a199203b29bfc460525c1f7b118164867df1` | 42283 |
| `resultados_revisor_6/cobertura_6.txt` | `9711f04` | `14935a19fc78ad59ee6530ade2fcb110ebcf0bae` | `aa209fc2889255bdae977135ef17fb8bdfc4ecb23a7118e6e59d2c60e199206c` | 10121 |
| `resultados_revisor_6/consultas_6.txt` | `9711f04` | `7d811b4a8807fc78dfb4b82061ed91a41a216518` | `e2e65edc43d4b7c3441b3e701b694f602f43ba7f3b584e34ee5cb022628e4dfe` | 15390 |
| `resultados_revisor_6/contraejemplos_6.txt` | `9711f04` | `8ce50839b036871e484baceb77735f73e13e7742` | `40ac803128a67e79b884c5691a78869ce672239850251d0deac261f2a0f754b8` | 22685 |
| `resultados_revisor_6/lectura_filas_c12.txt` | `9711f04` | `db07eeed1d5573a761cf573d24dcaf58aefa63d8` | `be602006a6d8e28b105263da41e7339546b937a39d158aaa3cfdba2becc1f043` | 33352 |
| `scripts_revisor_6/arnes6.py` | `9711f04` | `c25f1b56a0b7e215b28d9dce4626e9e5d9337471` | `a57454f19aff96492de9e2d3760ed62f673bb3dc7b243274c745c17198c56fd9` | 5347 |
| `scripts_revisor_6/barrido_6.py` | `9711f04` | `ed9a67fdfda238bc021dce65a2dae8822aa12965` | `63abb4d421774bd6e15b0cea5763da7d9719eb46112d3631bcc815786ac29829` | 9546 |
| `scripts_revisor_6/clases_6.py` | `9711f04` | `af8e2e2be97008998e7436d72539e08da44ee480` | `441dd630c401a1d2a581c68b98b653e579f3ca801b3bc19c67279b8a4cb064a2` | 19462 |
| `scripts_revisor_6/cobertura_6.py` | `9711f04` | `69a9084f61f4047f21b8cffe88d753de65116da0` | `b8fed218870f8c8c3e58763fdf71eacaec9036c441df2b72510e47d2b5ccd7d5` | 15062 |
| `scripts_revisor_6/consultas_6.py` | `9711f04` | `75759df495444c3979c7b5b6eea0d7b69ad09e0e` | `f2169572ac99b13e89cba07f25ef29b422d6cb2a110a80bcda2912fac0ae4365` | 8516 |
| `scripts_revisor_6/contraejemplos_6.py` | `9711f04` | `74e5028aec675e9a056435efdbc08b850e4fe247` | `828997e1ff584550be3c638d51ff0cd2c762ee59bd154aa3462c1b38fefdf313` | 11572 |
| `scripts_revisor_6/geom.py` | `9711f04` | `d43fcdf1c86c3dd324a99df616d76cf1f125dce2` | `d25aa008559c44ad1d2eb8a3d7dd7b52ed7171d1f24fc6c6cfffe0da605fe0af` | 9645 |
| `scripts_revisor_6/lectura_filas_c12.py` | `9711f04` | `71ea8cb18d8a01d01856de5da329a539aba7e942` | `d19a0036326ab5a8f9dc93ff4bf875c808a3818929232f9061100f3f8095662c` | 15720 |
| `scripts_revisor_6/lectura_geometrica.py` | `9711f04` | `635639d37682644a83b8bf3481278d489297e49c` | `abf869c17f4fde55d5214c07dc1bb31007d4f301e38c7a0be2f71cb51c4c700d` | 9297 |

Comprobación (desde la raíz del repositorio): `git diff --name-only 595d2f678178e41dac15e8d24b0523efe327b5b8 9711f04eba236c31100d0e3bd631b276c804e8c4 | while read p; do [ "$(git hash-object "$p")" = "$(git ls-tree 9711f04eba236c31100d0e3bd631b276c804e8c4 "$p" | awk '{print $3}')" ] && echo "OK $p" || echo "DISTINTO $p"; done`

## Revisión independiente n.º 7

Los 15 archivos de esta tabla proceden de la rama `auditoria/economica-f1-frente-e-revision`, commit `d192cab1153197df7d27dacb3f5d63c5fa030f8e` (padre `9711f04eba236c31100d0e3bd631b276c804e8c4`), publicado el 16 de noviembre de 2026 a las 04:18:26 UTC por una sesión de revisión nueva, distinta de las de las revisiones n.º 1, 3, 4, 5 y 6, y se copiaron sin cambios en las mismas rutas con `git show`. El material revisado es el commit congelado `c96d544646b2fa5a66c233402a9f31332a643cec` (C15) de la rama `auditoria/economica-f1-frente-e`.

| Ruta (relativa a revision/) | Commit del último cambio | Id de blob de git | SHA-256 | Bytes |
|---|---|---|---|---|
| `REVISION_INDEPENDIENTE_7.md` | `d192cab` | `14a9d776fa4927e91ff0dd115e048124c0d96437` | `bb1204d040fc4b522ea17fb5fa903a295778b41de20f73f5bb677b4c295d636f` | 56211 |
| `resultados_revisor_7/barrido_7.txt` | `d192cab` | `d82c0e4e95a706b0c332cfcf50303d190179939d` | `84e4e8d365fba410add891e80480a4464c16c77e82c45082b2ce460d559405af` | 2415 |
| `resultados_revisor_7/clases_7.txt` | `d192cab` | `7be552448e02c783abea177689ee04241921f5a8` | `1c9b34230d6ac7509648810369679ff9fb0b7e0741b4f2e713357075ced050e2` | 40550 |
| `resultados_revisor_7/contraejemplos_7.txt` | `d192cab` | `5bb52cd987c5e33a7d09520ea6d64d2aaae1ffdf` | `6fa7a6bb5404bb5a1da95943325e6915555c0ebd7b3531de07e836a6842e0c79` | 31745 |
| `resultados_revisor_7/lectura_filas_c14.txt` | `d192cab` | `c5b8a0c2a0d7e6898c95faffbedc9857cf891ce4` | `543bac584ee292912c8d0a09a2a5c56074b1934b2ff48c760d3178dbddc660b8` | 7681 |
| `resultados_revisor_7/reproduccion_7.txt` | `d192cab` | `0695845184ca95af1db8a83031a5e05f20565269` | `6feae5aaa942c8c9400d210c23eb9883de4592b35d55a25ce4d759429a68ec9c` | 5123 |
| `resultados_revisor_7/sondas_umbral_7.txt` | `d192cab` | `f284140217c8ab2f6192f67cffe533208da75c82` | `cf3e36e3d34112c714b555de4265cfa08db8287fab950aff5a8dcb9b8875144c` | 12459 |
| `scripts_revisor_7/arnes7.py` | `d192cab` | `c6fbab80f97a35f85c0a7494e65a2c2647480367` | `1a1d05442d109f7b16232f9c9961e178f92a9fbc5a13b54fe7b849b8a649aec6` | 7535 |
| `scripts_revisor_7/barrido_7.py` | `d192cab` | `f12c97fb27d4569386d40714cedf95142e606aae` | `b9d387e60a6cd011b75cf1c2bd12844f0706dc68601ec0a85211f2bbd43f65ff` | 14822 |
| `scripts_revisor_7/clases_7.py` | `d192cab` | `23590bf1edb01ce43fb6b0c7017d894e494118e9` | `2dac2950113e7e2950323da2073b4489b89218d8d137e7ca16cb4470a50ff70d` | 26730 |
| `scripts_revisor_7/contraejemplos_7.py` | `d192cab` | `95f625c63bff06257ea76bafa776d94b0807af7b` | `0ba40589a871c2c05b4b5d7e6df2bfc0729c2f00a55a51277f2e58ba96a40bd2` | 11458 |
| `scripts_revisor_7/geo7.py` | `d192cab` | `453f4a14ce65ef9178ab72dbbba682be85110598` | `968841e86df5a651dd9b1f944c9b212e7b2f8edfdf37c770862f6d751e5b154a` | 10530 |
| `scripts_revisor_7/lectura_filas_c14.py` | `d192cab` | `c7ce1981a4eeb77ba572ccc7f3a36b438b279b78` | `07d02dd31e8757c2ef988c54ae9ff8fa6778a85e022cad8881bde76ae9396f88` | 7757 |
| `scripts_revisor_7/reproduccion_7.py` | `d192cab` | `b1548b3e863ffa6407f8a6327f11c5c52f7406c0` | `ee3f864c64e056fe476d30f5c6fa78846d6ca04fd30bc10e2798aabdc26f4834` | 15038 |
| `scripts_revisor_7/sondas_umbral_7.py` | `d192cab` | `baddcbd76c3199781a144eb5a25a09e190158fa5` | `e00d72ff68d894e3f9322c258830864c8a9c7cac037a736b856a49410e8038d5` | 12363 |

Comprobación (desde la raíz del repositorio): `git diff --name-only 9711f04eba236c31100d0e3bd631b276c804e8c4 d192cab1153197df7d27dacb3f5d63c5fa030f8e | while read p; do [ "$(git hash-object "$p")" = "$(git ls-tree d192cab1153197df7d27dacb3f5d63c5fa030f8e "$p" | awk '{print $3}')" ] && echo "OK $p" || echo "DISTINTO $p"; done`

## Revisión independiente n.º 8

Los 18 archivos de esta tabla proceden de la rama `auditoria/economica-f1-frente-e-revision`, commit `3138a6b65aae12d94c9aa82b314e785322dec793` (padre `d192cab1153197df7d27dacb3f5d63c5fa030f8e`), publicado el 16 de noviembre de 2026 a las 06:40:38 UTC por una sesión de revisión nueva, distinta de las de las revisiones n.º 1, 3, 4, 5, 6 y 7, y se copiaron sin cambios en las mismas rutas con `git show`. El material revisado es el commit congelado `863ddde9190044690bfe4ee7c2a0d6fddc4c811a` (C17) de la rama `auditoria/economica-f1-frente-e`. `scripts_revisor_8/relanzar_revisores_6_7.sh` conserva el modo ejecutable (100755) que tiene en el commit de origen.

| Ruta (relativa a revision/) | Commit del último cambio | Id de blob de git | SHA-256 | Bytes |
|---|---|---|---|---|
| `REVISION_INDEPENDIENTE_8.md` | `3138a6b` | `897f01cf27f55f6c728f98d0d230f8de84d2751e` | `839487b6a4ec394379e5e484513de6b94fb9715bdca80969557199df00c4f72f` | 55167 |
| `resultados_revisor_8/barrido_8.txt` | `3138a6b` | `a6dc9cafca8fd5b2f877b17a15ff27d6bd5b882b` | `5014f914fcf4303207abe8a4e0313c205e98311594ffc83371b457be3774ba41` | 6736 |
| `resultados_revisor_8/clases_8.txt` | `3138a6b` | `35741c77e3b26d8c4cb0f62ad8c4d6394b747f41` | `0681118e8b64aa7ed4bc4dc3f4e9901d04767936a9920a94ceb161231ccc2117` | 69427 |
| `resultados_revisor_8/comparacion_6_7.txt` | `3138a6b` | `26c0334c924992a3a7b043b130c98d74a9433701` | `38366dd538eeaabe17360f5c224072aaa061716a1b257bc1d621f038ea0fdec6` | 2217 |
| `resultados_revisor_8/consultas_8.txt` | `3138a6b` | `7884e7303c9cf15b363a152b015c706ae39000bc` | `7259b5f7f132eeaeb6a70334774d1a67f39b2e4d804c8d3ac06ff7dd73553763` | 50518 |
| `resultados_revisor_8/contraejemplos_8.txt` | `3138a6b` | `ef7ddf65c3a8ef352ad2b6e3be4bcc48ac4282f9` | `3e63ad45785af66c6fc58882ce59f1e05f3f85d5d0362e20f6896413750fd508` | 26667 |
| `resultados_revisor_8/lectura_saldos_8.txt` | `3138a6b` | `330f24bbc470bce5fa8e11c0bc5c04a4556586fb` | `85f5460ac8a1fdc5ebf56b1c19835df0aa4e17e7dfb1461f87b9aee8d7ffb6e1` | 11208 |
| `resultados_revisor_8/reproduccion_8.txt` | `3138a6b` | `3486cd0b9a0caabb957bc5b93ac836b52ecef0b4` | `cf90cd5867daff9d69b12f0e713c832df17813a7668e2e1f2d2e849bc1c6f4ca` | 4286 |
| `resultados_revisor_8/sondas_8.txt` | `3138a6b` | `1027878d93e4b893fd78f916729fe38f3df21514` | `161750538734aa18549bebd56d948e632929fbc9274df79e79caf2fc8938fd7f` | 4389 |
| `scripts_revisor_8/arnes8.py` | `3138a6b` | `616c2696f0348ae7e096ec2de365a789fc117215` | `989032715e64cf913f7980c74476805bc177dac79cbe336731ac1f1715f673a8` | 5037 |
| `scripts_revisor_8/barrido_8.py` | `3138a6b` | `8f5561e5d7d112006f02927b99128b119ec5f122` | `d1609601ee824b5860e07353f61be0f0d6bfe27924ab43b0376dc36ff02128b4` | 15423 |
| `scripts_revisor_8/clases_8.py` | `3138a6b` | `7449204cca1210b8712961b4b02db3cb4eaed9df` | `35cde1339f77b3de6a7bcbe4fd9374598fa24c3f0650cf411448da234d7509f7` | 29795 |
| `scripts_revisor_8/consultas_8.py` | `3138a6b` | `f61cdefe3606358e816d8c6a27818552fadeaa21` | `f14f76167ee862b1fc58ff1e586ce5eb493446cc8e475c4c8893111e1190fb3c` | 18205 |
| `scripts_revisor_8/contraejemplos_8.py` | `3138a6b` | `053e4542215eda9a5fcd31743b7f29865fdc30fa` | `cfdbd7cdde875447792d69973194868931ee234243e398a41e71a8d8ebf8cf13` | 11897 |
| `scripts_revisor_8/lectura_saldos_8.py` | `3138a6b` | `d103445db399fffde61813f0551cb996b3763708` | `6df3e020164270b3e6b0af528e37aa4af0f0ad9e01655262237d52792e321966` | 5314 |
| `scripts_revisor_8/relanzar_revisores_6_7.sh` | `3138a6b` | `bcaafe461962ed46973c14d8e848a2e77dc64bb3` | `c4397f62918ffd5d0f4b1f64ae6030bf395bdd922b4666ccae1182fe43a9887b` | 4935 |
| `scripts_revisor_8/reproduccion_8.py` | `3138a6b` | `d12cac02c6e373097f844469dda444561284b565` | `55dd368f762482299e0e90fdafd60e8011fea0afec935dedc13f9a5fa055d469` | 11942 |
| `scripts_revisor_8/sondas_8.py` | `3138a6b` | `740049a4a1202a73d50d1278b5c191a4ed5d9c6e` | `51ec34e3e872b6c1fc505b93a52e13b805f4b70e56ad7266952e216040842ef8` | 9435 |

Comprobación (desde la raíz del repositorio): `git diff --name-only d192cab1153197df7d27dacb3f5d63c5fa030f8e 3138a6b65aae12d94c9aa82b314e785322dec793 | while read p; do [ "$(git hash-object "$p")" = "$(git ls-tree 3138a6b65aae12d94c9aa82b314e785322dec793 "$p" | awk '{print $3}')" ] && echo "OK $p" || echo "DISTINTO $p"; done`
