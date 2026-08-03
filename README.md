# Sistema-de-Reserva-de-Ingressos

# 🎬 Cinema Booking

Sistema de reserva de ingressos para uma **rede de cinemas**, desenvolvido com foco em **engenharia de software**, utilizando **Monólito Modular**, **Clean Architecture** e boas práticas de desenvolvimento.

O projeto tem como objetivo simular um sistema real de venda de ingressos, permitindo que usuários visualizem filmes, escolham sessões, selecionem assentos e realizem reservas de forma segura, tratando concorrência e reservas temporárias.

---

## Objetivos

* Desenvolver um sistema com arquitetura escalável e de fácil manutenção.
* Aplicar conceitos de Engenharia de Software durante todo o ciclo de desenvolvimento.
* Estudar e aplicar boas práticas de modelagem de domínio.
* Implementar mecanismos de concorrência para evitar reservas duplicadas.
* Construir um projeto completo para portfólio.

---

## Principais Funcionalidades

### Usuários

* Cadastro
* Login
* Recuperação de senha
* Gerenciamento de perfil
* Histórico de reservas

### Cinemas

* Listagem de cinemas
* Visualização de detalhes
* Programação por cinema

### Filmes

* Listagem de filmes
* Pesquisa
* Detalhes
* Trailer
* Sinopse

### Sessões

* Listagem de sessões
* Filtro por cinema e data
* Visualização da disponibilidade dos assentos

### Reservas

* Seleção de assentos
* Reserva temporária
* Confirmação da reserva
* Cancelamento da reserva
* Expiração automática
* Liberação automática dos assentos

### Ingressos

* Geração automática após confirmação da reserva
* Visualização do ingresso
* QR Code para validação

### Administração

* Gerenciamento de usuários
* Gerenciamento de cinemas
* Gerenciamento de filmes
* Gerenciamento de sessões
* Gerenciamento de reservas

---

## Tecnologias

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic
* JWT

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS

### Infraestrutura

* Docker
* Docker Compose
* GitHub Actions

---

## Arquitetura

O projeto será desenvolvido utilizando:

* Monólito Modular
* Clean Architecture
* SOLID
* Repository Pattern
* Dependency Injection

---

## Estrutura do Projeto

```text
cinema-booking/
│
├── backend/
├── frontend/
├── docs/
├── docker/
├── .github/
│   └── workflows/
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## Escopo do Projeto

O sistema representa uma **rede de cinemas**.

Algumas decisões de domínio adotadas:

* Catálogo de filmes compartilhado por toda a rede.
* Todas as salas utilizam o mesmo layout de assentos na primeira versão.
* Todos os assentos são do tipo comum.
* Reservas temporárias expiram automaticamente após 10 minutos.
* O ingresso é gerado automaticamente após a confirmação da reserva.
* O módulo de pagamentos será implementado em uma versão futura.

---

## Roadmap

* [x] Definição do escopo
* [x] Levantamento de requisitos
* [x] Modelagem do domínio
* [x] Casos de uso
* [ ] Modelo de domínio (DDD)
* [ ] Banco de dados
* [ ] API REST
* [ ] Estrutura do backend
* [ ] Estrutura do frontend
* [ ] Implementação
* [ ] Testes
* [ ] Docker
* [ ] CI/CD

---

## Objetivos de Aprendizado

Este projeto será utilizado para estudar e aplicar conceitos como:

* Estruturas de Dados
* Algoritmos
* Banco de Dados
* Backend
* Testes
* Design Patterns
* Clean Architecture
* Domain-Driven Design (DDD)
* Docker
* CI/CD
* Concorrência
* WebSockets
* Redis

---

## Licença

Este projeto foi desenvolvido para fins de estudo e portfólio.
