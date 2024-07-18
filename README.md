
# Chess Coop

Chess Coop is an online multiplayer chess game built with Vue.js for the frontend and Django for the backend. The project uses Docker for easy setup and deployment. It leverages `chess.js` for chess game logic and `chessboard.js` for the chessboard UI.


## Features

- Create and join chess rooms
- Play real-time multiplayer chess games
- Persistent game state using Redis
- Responsive UI built with Vuetify
- WebSocket support for real-time communication

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository:

```sh
git clone https://github.com/your-username/chess-coop.git
cd chess-coop
```
 
2. Build and run the Docker containers:

```sh
docker-compose up --build
```

3. Migrations

```sh
docker-compose run chesscoop_backend python manage.py migrate
```

4. Access the application:
Open your web browser and go to http://localhost:3000



```
chess-coop
├─ .git
│  ├─ COMMIT_EDITMSG
│  ├─ config
│  ├─ description
│  ├─ FETCH_HEAD
│  ├─ HEAD
│  ├─ hooks
│  │  ├─ applypatch-msg.sample
│  │  ├─ commit-msg.sample
│  │  ├─ fsmonitor-watchman.sample
│  │  ├─ post-update.sample
│  │  ├─ pre-applypatch.sample
│  │  ├─ pre-commit.sample
│  │  ├─ pre-merge-commit.sample
│  │  ├─ pre-push.sample
│  │  ├─ pre-rebase.sample
│  │  ├─ pre-receive.sample
│  │  ├─ prepare-commit-msg.sample
│  │  ├─ push-to-checkout.sample
│  │  ├─ sendemail-validate.sample
│  │  └─ update.sample
│  ├─ index
│  ├─ info
│  │  └─ exclude
│  ├─ logs
│  │  ├─ HEAD
│  │  └─ refs
│  │     ├─ heads
│  │     │  └─ main
│  │     └─ remotes
│  │        └─ origin
│  │           ├─ HEAD
│  │           └─ main
│  ├─ objects
│  │  ├─ 00
│  │  │  └─ f2a0d6cf936f2515aa24957cc599228f23a73f
│  │  ├─ 06
│  │  │  └─ 38c655b069d874c32fa6420cd73f0204172535
│  │  ├─ 09
│  │  │  └─ 83f02770a65cef9e085d4dad2e0801eeb99d09
│  │  ├─ 0e
│  │  │  ├─ 9f8bad38e179eebda8774e9da3c30113699ce7
│  │  │  └─ dc4896a66af3b9f4048d3d6f07e3600cd61188
│  │  ├─ 10
│  │  │  └─ cda25cfddf646e393e3ff832172a075e543f85
│  │  ├─ 19
│  │  │  └─ 04599739683b598001f007b4736659817b54fe
│  │  ├─ 1a
│  │  │  └─ 8c4e8bc35e2d5047cae2fd875fa96871d10451
│  │  ├─ 1d
│  │  │  └─ bd18abd95a6ae678b0dd036e7f44016ed5daf4
│  │  ├─ 1e
│  │  │  └─ d516bced13f12bbe8ecbf77e898fe6b1616782
│  │  ├─ 21
│  │  │  └─ 68bc18ff55f8e6f793a57132e0516e86c424e9
│  │  ├─ 24
│  │  │  └─ 549ecf446e3b368ccb7a28ca47fc1bb9ca04c1
│  │  ├─ 29
│  │  │  └─ 7dcd4b53c3a5cbe28c32ea5240b1e5b80fef5c
│  │  ├─ 2b
│  │  │  └─ f756dc6048b2956ac9a6e10d8aab7e4fe407fb
│  │  ├─ 2e
│  │  │  └─ 699b5845b14981508ec17ba45a67c94074188c
│  │  ├─ 32
│  │  │  └─ 68227ce827278a6e0cc9bd8bfc89be3b137c56
│  │  ├─ 33
│  │  │  ├─ 023c3dd008157504f26de175a54cee4e433e0e
│  │  │  ├─ 857c32d227951f09ec3c7c1cf5417f34665e8a
│  │  │  └─ ed729f7358607efb1258a7c2e3054be6b70e85
│  │  ├─ 36
│  │  │  └─ e4eb69b8dc29981b8b406afde7711e13c2d517
│  │  ├─ 37
│  │  │  └─ d8e6325f582d8197dd3dc5d2fa86c2616f21b8
│  │  ├─ 3c
│  │  │  └─ cbbd7de46fd1e7bf08baff2d855b46fe38eb4b
│  │  ├─ 3e
│  │  │  └─ a4f02743bfa8492f58ab40d8f85d263a979e27
│  │  ├─ 43
│  │  │  └─ e641c475507bb75ec5965ed974159af3f2b227
│  │  ├─ 4a
│  │  │  └─ aee2c3bd5dc26f5a1ce19f9548afcfabf04e20
│  │  ├─ 4d
│  │  │  └─ bb8293af03821eaf397e251ea3730918317efe
│  │  ├─ 4e
│  │  │  ├─ 059761c1499db8761fd720e2c158093f741e3e
│  │  │  └─ d7224826b7e8e62c9777e0124ee4f9f7a7f94d
│  │  ├─ 4f
│  │  │  └─ da5596a265454b3cf9678a90f46e7b9b8e52a1
│  │  ├─ 51
│  │  │  └─ b0164b899df07ab61362c3c563c9cab712ab93
│  │  ├─ 53
│  │  │  ├─ 9c8d8d6d5b0fb881c727e116700d192c490ce3
│  │  │  └─ f732feb11229045f35ea1d5400d97240a58693
│  │  ├─ 54
│  │  │  └─ 588d27141dbe2cc3dddc968cc5702a214e39ab
│  │  ├─ 55
│  │  │  └─ 7461ebd48cc0eef94465356e9b7de72cc8b4c2
│  │  ├─ 56
│  │  │  ├─ 1e44eac7c40a1723b794e4d5099c5ca426c84e
│  │  │  └─ d0ea5055f27c6f60fbd93b374d847c7dfaf574
│  │  ├─ 59
│  │  │  ├─ 711efe1be473aa8ba29fb5c20767dffcc4f340
│  │  │  └─ f1d58cfe36b17b9eed94b04c0a00d3bb8ef65f
│  │  ├─ 5a
│  │  │  ├─ 1f2d222a302a174e710614c6d76531b7bda926
│  │  │  └─ 7df30147cf6868e094bd8ee75bb6d076cb8b60
│  │  ├─ 5c
│  │  │  └─ 235b443d589fd4d3d0e624bf96287663c63803
│  │  ├─ 5d
│  │  │  └─ 1edc88b8b4d37cc3f5370e229fee8985f421d8
│  │  ├─ 5e
│  │  │  ├─ 81c314b8393449446955b9f5a226c48a9f0683
│  │  │  └─ f72a6eee803b0cefc7abcaf480069c4236ccfe
│  │  ├─ 60
│  │  │  ├─ 07ee2e5781406155d06f3c48c74924ba5bc182
│  │  │  └─ bfa46be5df4c4e1d535816f3479b7d439c3ba6
│  │  ├─ 62
│  │  │  └─ 094470c27c634087556460f0182a36b8adeb2d
│  │  ├─ 66
│  │  │  └─ e23359c3dabfe3929b4e2fa049c41037afb15f
│  │  ├─ 67
│  │  │  └─ b8317061b926d8b3838ee51e8ae23a96c1979d
│  │  ├─ 69
│  │  │  └─ 236d4a3ee99139ea091e5d0f553898c20322b6
│  │  ├─ 6d
│  │  │  ├─ 573b2fc8d8551becb9a0c1780bbf64b76f8b10
│  │  │  └─ feb02d7a926865858000a9421ecc9565c1633b
│  │  ├─ 74
│  │  │  └─ be2ec692b6ae113645253c194b78a6a311107a
│  │  ├─ 75
│  │  │  ├─ 623f4f416c727d59610abf32797192b0d5f381
│  │  │  ├─ 65660356e5b3723c9c33d508b830c9cfbea29f
│  │  │  └─ bb094ec3cc2366b4448d4848bf5aff0a157ac9
│  │  ├─ 76
│  │  │  └─ e02132c5adf152b0cb9dcc6a4dfe6253bd4d14
│  │  ├─ 77
│  │  │  └─ 8bab6d4d321baaad12a8bb8ee2a989093828e9
│  │  ├─ 7a
│  │  │  ├─ 3d653e1b263496bc3897fa4e959ae670e75eca
│  │  │  └─ 867a28f0bb6e130b781b17b182d2d77e170b92
│  │  ├─ 7c
│  │  │  └─ e503c2dd97ba78597f6ff6e4393132753573f6
│  │  ├─ 80
│  │  │  └─ dad2d21f9d280871fdfa2f4bb26394a2de7323
│  │  ├─ 81
│  │  │  └─ d16e849aef676476e83d701358103a2d64694a
│  │  ├─ 83
│  │  │  └─ 8fab180b6443ff5d6f3e8f97df74c4ed39e56d
│  │  ├─ 88
│  │  │  └─ 16868a41b651f318dee87c6784ebcd6e29eca1
│  │  ├─ 8a
│  │  │  └─ ec93bf5196ce009e28eeb064c16cdd9c5dad93
│  │  ├─ 8b
│  │  │  └─ 137891791fe96927ad78e64b0aad7bded08bdc
│  │  ├─ 8c
│  │  │  └─ 38f3f3dad51e4585f3984282c2a4bec5349c1e
│  │  ├─ 8e
│  │  │  └─ f33ebb654a0ad375b5e90c3a8ec8ffab0f898a
│  │  ├─ 91
│  │  │  └─ 2b6717ab02d8154b835a6800224ab3dadcf5b8
│  │  ├─ 92
│  │  │  └─ 5f229e113447be24d0f8f6637acd754a27b501
│  │  ├─ 94
│  │  │  └─ 2f1b7d00c20b6bbba17e723eda0f6aa65f9173
│  │  ├─ 97
│  │  │  └─ 3dd97fea384869f29a7932f2ec82beed0a650c
│  │  ├─ 98
│  │  │  └─ 27ad6a50a0c6199c3b72581cfb5403ed017153
│  │  ├─ 99
│  │  │  └─ 1a1f3a7b6cd2d223ed55a1822314a612d48771
│  │  ├─ 9b
│  │  │  └─ edaca9ff1de71ca19a5fcc160940bc18339efa
│  │  ├─ a7
│  │  │  └─ 59945e5961b51712723001e13f83c6d85d3ac3
│  │  ├─ a8
│  │  │  ├─ 0ec31a28d0997f6d0a9554c603a0474fefc7aa
│  │  │  └─ 703b254fabc9c32a1e149d4058acbc1b8cbf91
│  │  ├─ a9
│  │  │  └─ 6ba1e92d5db7686e57b6cd2d6ced6c6232d96a
│  │  ├─ ab
│  │  │  └─ 2944d432dd31a798f37dbf77b3bbd47ad663de
│  │  ├─ ae
│  │  │  ├─ 0219952f46d33d8c16b03fb3b8f21b9299b821
│  │  │  ├─ 1fd4be1c7f7ca557bfecbab394ad111df1c0f4
│  │  │  └─ 40def9877b1b661c4c4e48572714072e5eeb4b
│  │  ├─ b2
│  │  │  └─ 301d48757dbfb2da77d2aca4487ae33333951d
│  │  ├─ b5
│  │  │  └─ 57d028f9b6ef2ec01cead707803282b07a636a
│  │  ├─ b6
│  │  │  ├─ 4731a0fe8c67d765f3a3cce1e401fe57d9d2a0
│  │  │  └─ 672a6edf7bb8f373bbd97229885b25015ebf67
│  │  ├─ b8
│  │  │  ├─ 4ef52f2defc010f8c8794fb2084afd518746b4
│  │  │  └─ b23c63371b591a856ba799fd7d12fc20d37895
│  │  ├─ be
│  │  │  └─ 228ff42eca62cbb1b78196c2241ee2202c7c11
│  │  ├─ bf
│  │  │  └─ 5e4f9b8af567ada476f0d370523f5d97cb8550
│  │  ├─ c2
│  │  │  └─ 513ca0885db5a525f56ea1ccb6c8596d19c42c
│  │  ├─ c8
│  │  │  └─ 39ab1a0f92e1690fa493f774c0143efd263eef
│  │  ├─ cb
│  │  │  └─ d91f67f7a9cb2651c5d8e8b8c93a7caeb95c3a
│  │  ├─ cc
│  │  │  └─ 07597e035cd5e47d91849099f59feb1c532da3
│  │  ├─ cd
│  │  │  └─ 0be930df87e2a527f7ebadc6a4a13edd7b4e52
│  │  ├─ ce
│  │  │  └─ 289058cbd1d072f9958d092a8d2de31d334e48
│  │  ├─ d2
│  │  │  └─ 7f76be470d321b8502030177c7684ba34e4d9b
│  │  ├─ d7
│  │  │  └─ 7f10a1ead73b63f2a72b6db7de9b3d998cc87f
│  │  ├─ d8
│  │  │  ├─ 7192870ed24277e8ea8e39a58153c16753c16c
│  │  │  └─ d010a16fe71506ce962ec7d32d255629a804b0
│  │  ├─ db
│  │  │  └─ d3cd1a4fff82ddbc143a3108bd7c7cb066f7a5
│  │  ├─ df
│  │  │  └─ a6d337f341782262faef54c920ef5a7d6bee60
│  │  ├─ e0
│  │  │  ├─ 8379c1378ece14166a9a0ba69911fa81b65b95
│  │  │  └─ f0c99959c5e5143ead69f99d2fa7f6fe5a5ca5
│  │  ├─ e3
│  │  │  └─ de954676d010883fa4d7b52cfdab95b78064e2
│  │  ├─ e5
│  │  │  └─ 224490e0cefcc41f0a305183dd4ef4a91a95de
│  │  ├─ e6
│  │  │  └─ 9de29bb2d1d6434b8b29ae775ad8c2e48c5391
│  │  ├─ eb
│  │  │  └─ 0e296bc40b04cfb2b815bf1bcd73b5b9b2113d
│  │  ├─ ec
│  │  │  └─ cf7ce528e85ba67d9cf5b11f5a21a2ac298ea6
│  │  ├─ f2
│  │  │  ├─ 3bb49cd6e41cf28d9df7db462079895e3c4de4
│  │  │  └─ 6eb94b69f5fdbeeb3e85844b39e0b8c9181ecf
│  │  ├─ f5
│  │  │  └─ b080fa371977a319cedfeaa5211c9c9bc8ac10
│  │  ├─ f6
│  │  │  └─ 417d322cbb4239baf09e8d531bc1893405a946
│  │  ├─ f9
│  │  │  └─ 51a46a5a13fd5e496f5a49b94e9117c85001cb
│  │  ├─ fe
│  │  │  └─ 28253735aff6413ec5f561f0e1ffad7a2a2241
│  │  ├─ info
│  │  └─ pack
│  ├─ ORIG_HEAD
│  └─ refs
│     ├─ heads
│     │  └─ main
│     ├─ remotes
│     │  └─ origin
│     │     ├─ HEAD
│     │     └─ main
│     └─ tags
├─ .gitignore
├─ backend
│  ├─ base
│  │  ├─ asgi.py
│  │  ├─ settings.py
│  │  ├─ urls.py
│  │  ├─ wsgi.py
│  │  └─ __init__.py
│  ├─ chess
│  │  ├─ admin.py
│  │  ├─ apps.py
│  │  ├─ consumers.py
│  │  ├─ migrations
│  │  │  ├─ 0001_initial.py
│  │  │  └─ __init__.py
│  │  ├─ models.py
│  │  ├─ redis_utils.py
│  │  ├─ routing.py
│  │  ├─ serializers.py
│  │  ├─ tests.py
│  │  ├─ urls.py
│  │  ├─ views.py
│  │  └─ __init__.py
│  ├─ dockerfile
│  ├─ manage.py
│  └─ requirements.txt
├─ docker-compose.yml
├─ frontend
│  ├─ .eslintrc.cjs
│  ├─ .prettierrc.json
│  ├─ dockerfile
│  ├─ index.html
│  ├─ jsconfig.json
│  ├─ package.json
│  ├─ public
│  ├─ README.md
│  ├─ src
│  │  ├─ App.vue
│  │  ├─ assets
│  │  │  ├─ base.css
│  │  │  ├─ logo.svg
│  │  │  ├─ main.css
│  │  │  └─ pawn
│  │  │     ├─ b_bishop_1x.png
│  │  │     ├─ b_king_1x.png
│  │  │     ├─ b_knight_1x.png
│  │  │     ├─ b_pawn_1x.png
│  │  │     ├─ b_queen_1x.png
│  │  │     ├─ b_rook_1x.png
│  │  │     ├─ w_bishop_1x.png
│  │  │     ├─ w_king_1x.png
│  │  │     ├─ w_knight_1x.png
│  │  │     ├─ w_pawn_1x.png
│  │  │     ├─ w_queen_1x.png
│  │  │     └─ w_rook_1x.png
│  │  ├─ components
│  │  │  ├─ Chat.vue
│  │  │  ├─ ChessBoard.vue
│  │  │  └─ Snackbar.vue
│  │  ├─ composables
│  │  ├─ main.js
│  │  ├─ router
│  │  │  └─ index.js
│  │  ├─ services
│  │  │  └─ api.js
│  │  ├─ stores
│  │  │  └─ gameStore.js
│  │  └─ views
│  │     ├─ GameRoomView.vue
│  │     └─ HomeView.vue
│  └─ vite.config.js
└─ README.md

```