# 📡 Net Speed Monitor

**The ultimate automated network performance logger for your Discord Server.** *Track uptime, latency, and bandwidth speeds effortlessly.*

---

<div align="center">

  [![Discord](https://img.shields.io/badge/Discord-Add%20Bot-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/oauth2/authorize?client_id=1453503581067022559&permissions=51200&integration_type=0&scope=bot+applications.commands)
  [![Python](https://img.shields.io/badge/Made%20With-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![Status](https://img.shields.io/badge/Status-Online-success?style=for-the-badge)]()

</div>

---

## 🚀 Overview

**Net Speed Monitor** is a powerful utility bot designed to keep an eye on your network's health. Whether you are monitoring a home server, a Raspberry Pi, or just want to log your ISP's performance, this bot does it all automatically.

It runs periodic speedtests and posts beautiful, easy-to-read reports directly to a channel of your choice.

## ✨ Key Features

* **📊 Automated Monitoring:** Set it and forget it. The bot runs speedtests at intervals you define (e.g., every hour).
* **📉 Detailed Analytics:** Logs **Download**, **Upload**, and **Ping** (Latency) with high precision.
* **🎨 Smart Embeds:** Beautifully formatted reports with color-coded health indicators (Green for good speeds, Red for drops).
* **⚡ Instant Manual Tests:** Need to check the speed right now? Use `/testnow`.
* **🔒 Privacy Focused:** All data is processed locally on the host machine and sent only to your configured channel.

---

## 🖼️ Preview

Here is how a report looks in your server:

> **📡 Network Speed Report**
>
> **⬇️ Download:** `350.42 Mbps`
> **⬆️ Upload:** `45.12 Mbps`
> **📶 Ping:** `12 ms`
>
> *Automated Monitor running on Raspberry Pi*

---

## 🛠️ Commands

All commands are modern **Slash Commands**. Just type `/` and select the bot!

| Command | Description |
| :--- | :--- |
| **/setup** | Configure the logging channel and time interval (Admin only). |
| **/testnow** | Force an immediate speedtest and see results instantly. |

### Example Usage:
/setup channel:#network-logs interval:60

*(This will set the bot to post results in `#network-logs` every 60 minutes)*

---

## 🔗 Add to Your Server

Ready to monitor your network? Click the button below to authorize the bot.

### [👉 Click Here to Invite Net Speed Monitor](YOUR_INVITE_LINK_HERE)

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/CrazyAlex15">CrazyAlex</a></sub>
</div>