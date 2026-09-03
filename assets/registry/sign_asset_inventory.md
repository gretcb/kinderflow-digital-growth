# Kinder Signs Asset Inventory

Generated deterministically by `tools/build_sign_asset_registry.py` from the canonical registry.
External source files are inspected in place and are never copied into this repository.

## Validation summary

- Canonical signs: more, help, eat, sleep, milk, water
- Registered assets: 56
- Missing registered assets: 0
- Product-blocking reference gap: none.
- Registry validation: PASS (a documented product gap is not a malformed registry).

## Sign packages

| Sign | Labels | Input | Gemini demo | Technical | Visual | Printable | School |
| --- | --- | --- | --- | --- | --- | --- | --- |
| more | MORE / MÁS | present | AVAILABLE_PREGENERATED_DEMO_ONLY | REFERENCE_INPUT_AVAILABLE_NOT_ANALYSED_IN_CANONICAL_RUN | SOURCE_GROUNDED_OPTIONS_NEED_HUMAN_REVIEW | BLOCKED | UNAVAILABLE |
| help | HELP / AYUDA | present | AVAILABLE_PREGENERATED_DEMO_ONLY | REFERENCE_INPUT_AVAILABLE_NOT_ANALYSED_IN_CANONICAL_RUN | SOURCE_GROUNDED_OPTIONS_NEED_HUMAN_REVIEW | BLOCKED | UNAVAILABLE |
| eat | EAT / COMER | present | NOT_AVAILABLE_STATIC_FLOW_ALLOWED | REFERENCE_INPUT_AVAILABLE_SIGN_AWARE_REVIEW_NOT_CANONICAL_EVIDENCE | SOURCE_GROUNDED_OPTIONS_NEED_HUMAN_REVIEW | BLOCKED | UNAVAILABLE |
| sleep | SLEEP / DORMIR | present | NOT_AVAILABLE_STATIC_FLOW_ALLOWED | REFERENCE_INPUT_AVAILABLE_NOT_ANALYSED_IN_CANONICAL_RUN | SOURCE_GROUNDED_OPTIONS_NEED_HUMAN_REVIEW | BLOCKED | UNAVAILABLE |
| milk | MILK / LECHE | present | AVAILABLE_PREGENERATED_DEMO_ONLY | REFERENCE_INPUT_AVAILABLE_NOT_ANALYSED_IN_CANONICAL_RUN | SOURCE_GROUNDED_OPTIONS_NEED_HUMAN_REVIEW | BLOCKED | UNAVAILABLE |
| water | WATER / AGUA | present | NOT_AVAILABLE_STATIC_FLOW_ALLOWED | SUPPORTING_REFERENCE_IDENTITY_CONFIRMED_REVIEW_NEEDED | SOURCE_GROUNDED_OPTIONS_NEED_HUMAN_REVIEW | BLOCKED | UNAVAILABLE |

## File inventory

| Asset ID | Class | Sign mapping | Exists | Bytes | SHA-256 | Relative path |
| --- | --- | --- | --- | ---: | --- | --- |
| `canonical_sign_content` | KINDERFLOW_RUNTIME_ASSET | more, help, eat, sleep, milk, water | yes | 15176 | `1cdbb3d551076604ac01ea6429e063122a7dff97e7c54a3b75a71e2236adf3f1` | `prototype/data/signs.json` |
| `visual_sign_packages` | KINDERFLOW_RUNTIME_ASSET | more, help, eat, sleep, milk, water | yes | 40981 | `1138082a53af304f5a1b55baa21484f6cbd696d1212f2ac3cb531f10c4f8350b` | `prototype/data/visual_sign_packages.json` |
| `open_peeps_bust_base` | THIRD_PARTY_REFERENCE | more, help, eat, sleep, milk, water | yes | 26663 | `b631d9ab4a7bb7d0f632ffb42185825d4cf208853eb2c07338a15cc4999601df` | `../resources/Flat Assets/Separate Atoms/a person/bust.svg` |
| `open_peeps_arm_reference` | THIRD_PARTY_REFERENCE | more, help, eat, sleep, milk, water | yes | 44256 | `2e354cb71804158d4b5fa9ab8a6721c5cff1b74461990e911e1b2a2cf2e79ef0` | `../resources/Flat Assets/Templates/Bust/peep-4.svg` |
| `open_peeps_pointing_finger_reference` | THIRD_PARTY_REFERENCE | more, help, eat, sleep, milk, water | yes | 25007 | `b5fc22a9f2f5b2229b789e49587c6998564fa7b524f4b1107e3c25b640c12fd0` | `../resources/Flat Assets/Separate Atoms/pose/standing/pointing_finger-1.svg` |
| `functional_more` | FOUNDER_PROVIDED_REFERENCE | more | yes | 108814 | `b11d125a41b4ee5ea180361c7dc0f359d72ae366517128ae8a25664a3083408c` | `../resources/ilustraciones/more.jpg` |
| `functional_help` | FOUNDER_PROVIDED_REFERENCE | help | yes | 42007 | `079370a2bd6e301c64d29cc16a99ca09ec15af304330e3a77a30b7d351f4ee28` | `../resources/ilustraciones/help.jpg` |
| `functional_eat` | FOUNDER_PROVIDED_REFERENCE | eat | yes | 146232 | `9dac1ea686fc24a33b2ab3c088191cdc26ac1b8bed52e0e17d3f37b0b979a120` | `../resources/ilustraciones/eat.jpg` |
| `functional_sleep` | FOUNDER_PROVIDED_REFERENCE | sleep | yes | 28910 | `7fbdd8145fa0524d86c2d9c6c1bce57e148c24c01f2e501486f1c592248ce6bc` | `../resources/ilustraciones/sleep.jpg` |
| `functional_milk` | FOUNDER_PROVIDED_REFERENCE | milk | yes | 28482 | `e6e815f0f03fb83a99ecba03d8f4d3fb920ac1b85174b3739a7152817a9d9801` | `../resources/ilustraciones/milk.jpg` |
| `functional_hand_sheet_jpg` | FOUNDER_PROVIDED_REFERENCE | more, help, eat, sleep, milk, water | yes | 1378160 | `315bdee7269e14711ca0290283a4afdc34569026914d3db900af8a38516351da` | `../resources/ilustraciones/illustraciones_signos.jpg` |
| `functional_hand_sheet_eps` | FOUNDER_PROVIDED_REFERENCE | more, help, eat, sleep, milk, water | yes | 3475398 | `617281bfbdcb342183cd4eb2de55297304cebdbc428127e49a10371314cff01b` | `../resources/ilustraciones/vectores_illustraciones.eps` |
| `input_more` | FOUNDER_PROVIDED_REFERENCE | more | yes | 502934 | `9b3fe8f0880fef85f64264f34509aa70fb5c188a316be135cf5230af0009b594` | `../resources/video_input/more.mp4` |
| `input_help` | FOUNDER_PROVIDED_REFERENCE | help | yes | 1048227 | `344bfa462eb5d3eb5438b9c8981554e925a89d89aa4ffa3ac946a00b42cc3002` | `../resources/video_input/help.mp4` |
| `input_eat` | FOUNDER_PROVIDED_REFERENCE | eat | yes | 550619 | `90432a597ea75a02bdbb1cc903c1c09e64646565ab48394cd67d4da3f7477822` | `../resources/video_input/eat.mp4` |
| `input_sleep` | FOUNDER_PROVIDED_REFERENCE | sleep | yes | 544897 | `e423863518bcfc1e937d5207f98057976a089689987d52603f3fbf97355f0610` | `../resources/video_input/sleep.mp4` |
| `input_milk` | FOUNDER_PROVIDED_REFERENCE | milk | yes | 831970 | `1a525a1685cbf9aad9006168ca59f3df43856bdc5916764e8cc6555ea95c5760` | `../resources/video_input/milk.mp4` |
| `demo_more` | PREGENERATED_DEMO_OUTPUT | more | yes | 3721728 | `adec2ddda3b6cd8ce0a10e9eaa8a5eaf02f826147c0ea33fcc3be403ee48f6a4` | `../resources/video_output/mas.mp4` |
| `demo_help` | PREGENERATED_DEMO_OUTPUT | help | yes | 547216 | `529b3bea31746d8a1ce305828244badfa9db543ae1960312ad7c6665b838db02` | `../resources/video_output/ayuda.mp4` |
| `demo_milk` | PREGENERATED_DEMO_OUTPUT | milk | yes | 530320 | `55d106d20318c9c9be430f523a71e4b85d5a7656c90c4fdbdf32a58d1efa95c2` | `../resources/video_output/leche.mp4` |
| `flashcard_more_reference` | FOUNDER_PROVIDED_REFERENCE | more | yes | 2696928 | `92e41f7e68c44ec99c6f0c80537e089a0a02413672007bd3d1c2cd99252fcf89` | `../resources/flashcards/more-flash-card.pdf` |
| `flashcard_help_reference` | FOUNDER_PROVIDED_REFERENCE | help | yes | 650516 | `a28c72750a1e58aede191aa00ca18f509c47411c6755421245c4430a2010f6d0` | `../resources/flashcards/help-flash-card.pdf` |
| `flashcard_eat_reference` | FOUNDER_PROVIDED_REFERENCE | eat | yes | 2044069 | `2037609b3e510e937be803efaf0db007c9ab4bcb836f9b73745a6a0b4e2759dc` | `../resources/flashcards/eat-flash-card.pdf` |
| `flashcard_sleep_reference` | FOUNDER_PROVIDED_REFERENCE | sleep | yes | 2847495 | `f03467890345dd1fef060b226c9350a5559100176a49626438f1c2bc09aeb82f` | `../resources/flashcards/sleep-flash-card.pdf` |
| `flashcard_milk_reference` | FOUNDER_PROVIDED_REFERENCE | milk | yes | 1027607 | `026f09787ec453b72da11969e4c69f937566a707b4a0d79673c565e8fd6427ad` | `../resources/flashcards/milk-flash-card.pdf` |
| `icon_help_primary` | FOUNDER_PROVIDED_REFERENCE | help | yes | 30521 | `41b8da9ccb9099f64a354729e9e5dbe393357a866b39c1f2687b9645cde22b61` | `../resources/iconos/ayuda.png` |
| `icon_help_alternate` | FOUNDER_PROVIDED_REFERENCE | help | yes | 18568 | `ef7a1adf68645fcd0b5582b70da84dd9ba59ac5db655b933ba2e806b7c675415` | `../resources/iconos/ayuda2.png` |
| `icon_milk` | FOUNDER_PROVIDED_REFERENCE | milk | yes | 8060 | `2783bce03bdc11f10a56e4986743fe614c082033bdac2ccf9472d1e1ff2fb319` | `../resources/iconos/biberon.png` |
| `icon_eat` | FOUNDER_PROVIDED_REFERENCE | eat | yes | 22629 | `6b11ff5992a3f3e2cd76b39591912f3ced49c48963cb1a7b8614d4d68af897bb` | `../resources/iconos/comer.png` |
| `icon_sleep` | FOUNDER_PROVIDED_REFERENCE | sleep | yes | 21174 | `f38884e3261495e0ff4879679f8a4d8632cd53c2c553bd392467fde3f4dc7bc1` | `../resources/iconos/dormir.png` |
| `icon_more_play` | FOUNDER_PROVIDED_REFERENCE | more | yes | 26070 | `c4e72af6183b8ad8ff3cd1a5a524cce7ed5390b782c416b6a924df32b92be609` | `../resources/iconos/jugar.png` |
| `more_context_image` | KINDERFLOW_RUNTIME_ASSET | more | yes | 2126130 | `d364e1011347193ce2b14010bb324be08a970d1fab075a0448e84cf2f4376f52` | `prototype/assets/context/more-snack-time.png` |
| `input_water` | FOUNDER_PROVIDED_REFERENCE | water | yes | 586766 | `28f844d5af72ef1bcd351048ba57d74b2ad32bb6584fed919e27d3e59f8f44ea` | `../resources/video_input/water.mp4` |
| `functional_water` | FOUNDER_PROVIDED_REFERENCE | water | yes | 39108 | `aa56ca59a37f2e3b5cf188e34d7b747bc0855ddc85b2712bc13e8a760606fbbc` | `../resources/ilustraciones/water.jpg` |
| `flashcard_water_reference` | FOUNDER_PROVIDED_REFERENCE | water | yes | 1988888 | `af80d56706b4110ac1378f428806478b17669ace8a612a278cdee3a15729cbd9` | `../resources/flashcards/water-flash-card.pdf` |
| `water_landmark_summary` | TECHNICAL_EVIDENCE | water | yes | 11006 | `feb413fc233610f95f6dc962c9f6d6a6dd44412479ea78dd9345f084bfc6fef3` | `poc/output/diagnostics/sign_reference_motion_summary.json` |
| `water_detection_timeline` | TECHNICAL_EVIDENCE | water | yes | 34213 | `23c44d531370b1e16ad859cde3165a1efca36258a04cc6e27a7c9a3162504f6b` | `poc/output/diagnostics/sign_reference_detection_timeline.png` |
| `water_validation_summary` | TECHNICAL_EVIDENCE | water | yes | 854 | `7d4101ca5203e27a890426580fd5369f8537366a180b88f5d675887e47b3cc66` | `poc/output/validation_summary.json` |
| `static_more_a` | KINDERFLOW_DERIVED_ASSET | more | yes | 36338 | `cb138b8a2a626462098b3c015cfdf76ae062a52a267bf218b6ef9a84fbb82900` | `prototype/assets/signs/more-a.svg` |
| `static_more_b` | KINDERFLOW_DERIVED_ASSET | more | yes | 69118 | `b3229ed4d8828c573d08db8432be5083518e26d5fa145617f75ec6af646b832c` | `prototype/assets/signs/more-b.svg` |
| `static_more_c` | KINDERFLOW_DERIVED_ASSET | more | yes | 36327 | `76783fb92c6c7aafdef36ffa3280bbd5e19c5c61998fecf99bad8ba6804b381f` | `prototype/assets/signs/more-c.svg` |
| `static_help_a` | KINDERFLOW_DERIVED_ASSET | help | yes | 36113 | `97554ab2bf5e47f7c3b25e7eb64d9f114e3fe488362dd5b906e4c41c348c7aac` | `prototype/assets/signs/help-a.svg` |
| `static_help_b` | KINDERFLOW_DERIVED_ASSET | help | yes | 68682 | `e7e44db0f71b7420e81b1bbe6cd08faa43445c19316551b9f5c0c2889aa4ea16` | `prototype/assets/signs/help-b.svg` |
| `static_help_c` | KINDERFLOW_DERIVED_ASSET | help | yes | 36117 | `b3d9c6da7636084fcf8df9827323a2bfd63e002c9fbe9c03579a6b08e69745b4` | `prototype/assets/signs/help-c.svg` |
| `static_eat_a` | KINDERFLOW_DERIVED_ASSET | eat | yes | 33746 | `92747ef417eaccade25ea8c845b6d865e130509e233fdd9073528e6c404932a9` | `prototype/assets/signs/eat-a.svg` |
| `static_eat_b` | KINDERFLOW_DERIVED_ASSET | eat | yes | 63952 | `c131cbb16db8fc4c0c388d7bf71a13350d4fc2e7fd830afce068b731d0319edc` | `prototype/assets/signs/eat-b.svg` |
| `static_eat_c` | KINDERFLOW_DERIVED_ASSET | eat | yes | 33742 | `7157ea6018632a6561288a45bdeb7be36b357a01c1309c7163e2daded8de917f` | `prototype/assets/signs/eat-c.svg` |
| `static_sleep_a` | KINDERFLOW_DERIVED_ASSET | sleep | yes | 33683 | `08509011ec42593621473c96c5600d599f415a562841c774ef60245598da3a48` | `prototype/assets/signs/sleep-a.svg` |
| `static_sleep_b` | KINDERFLOW_DERIVED_ASSET | sleep | yes | 63756 | `fd02fea1c890ef3dec52f8646b1394f1a49b63aae83c161c7d53721038e8b8f5` | `prototype/assets/signs/sleep-b.svg` |
| `static_sleep_c` | KINDERFLOW_DERIVED_ASSET | sleep | yes | 33688 | `206e064a359d43dbd65eb2dd17b0fa7f3275f88ebf147927ddc609fb4cc6f457` | `prototype/assets/signs/sleep-c.svg` |
| `static_milk_a` | KINDERFLOW_DERIVED_ASSET | milk | yes | 33920 | `b33f99a2c4b0000be73509048f9cb76e5df5024394537a151a4fb05bcc580bd5` | `prototype/assets/signs/milk-a.svg` |
| `static_milk_b` | KINDERFLOW_DERIVED_ASSET | milk | yes | 64256 | `8c2d7928647dc8134d4aa5e48ce1051d93f54cfe76980dc6b05f10bace855030` | `prototype/assets/signs/milk-b.svg` |
| `static_milk_c` | KINDERFLOW_DERIVED_ASSET | milk | yes | 33934 | `2675f2f7b37c63f9076c2a4e81db4f264b58d97d159de3b42027c61134252f0e` | `prototype/assets/signs/milk-c.svg` |
| `static_water_a` | KINDERFLOW_DERIVED_ASSET | water | yes | 33980 | `eead4af19ff8fcb83aa8e692b124f86a9b54020f483c8c0355a99d7cfccb4e4c` | `prototype/assets/signs/water-a.svg` |
| `static_water_b` | KINDERFLOW_DERIVED_ASSET | water | yes | 64175 | `11a25cb3f24e070b1cb824c9ba854849996f138ae5b95493f2bcd2ec0e06f354` | `prototype/assets/signs/water-b.svg` |
| `static_water_c` | KINDERFLOW_DERIVED_ASSET | water | yes | 33974 | `c2fdbbcd4fe912abfa37257702429fe27d5c8b796c69fd21bac2b440482ecaef` | `prototype/assets/signs/water-c.svg` |

## Guardrails

- Open Peeps defines character identity only; functional references define sign mechanics.
- The exact registered `pointing_finger-1.svg` atom defines hand-style grammar only; `Separate Atoms/body/Pointing Up.svg` is not a substitute.
- Gemini FX files are pre-generated demo outputs, not reference inputs, current-run products, or linguistic certification.
- Reference flashcards and vendor routine icons cannot enter printable outputs.
- EAT, SLEEP and WATER intentionally have no Gemini FX output and remain eligible for the local static workflow.
