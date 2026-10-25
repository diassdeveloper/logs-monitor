# Logs Monitor

Monitor de arquivos de log em tempo real desenvolvido em Python, com identificação de mensagens críticas e envio de alertas por e-mail.

## Funcionalidades

- Monitoramento de arquivos de log em tempo real.
- Identificação de mensagens `ERROR`, `WARNING` e `CRITICAL`.
- Envio de alertas por e-mail.
- Configuração do caminho do log e do intervalo entre alertas.
- Encerramento seguro com `Ctrl + C`.

## Tecnologias utilizadas

- Python
- Watchdog
- SMTP
- Variáveis de ambiente com `.env`

## Requisitos

- Python instalado.
- Conta de e-mail configurada para envio de alertas.

## Instalação

Clone o repositório e acesse a pasta do projeto:

```bash
git clone https://github.com/diassdeveloper/logs-monitor
cd logs-monitor
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie seu arquivo `.env` a partir do modelo:

```powershell
Copy-Item .env.example .env
```

Edite o `.env` com as configurações exigidas pelo projeto. Nunca compartilhe suas credenciais ou publique o arquivo `.env`.

## Execução

Para iniciar o monitoramento:

```bash
python main.py
```

Para especificar outro arquivo de log:

```bash
python main.py --log .\logs\teste.log
```

Para configurar o intervalo entre alertas:

```bash
python main.py --rate-limit 120
```

Pressione `Ctrl + C` no terminal para encerrar o monitoramento.

## Segurança

As credenciais devem ser mantidas no arquivo `.env`, que não deve ser enviado ao GitHub. Utilize o `.env.example` como modelo, sem inserir senhas ou tokens reais.

## Licença

Ainda não definida.
