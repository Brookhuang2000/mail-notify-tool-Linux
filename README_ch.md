# 邮件助手

一个轻量级 Python 工具，适用于科研或服务器环境中，自动执行命令并通过邮件进行结果通知和日志传送。同时支持查看收件箱内容和下载附件。

## 📌 功能特点

- ✅ 自动运行命令并发送日志邮件通知
- ✅ 手动发送邮件（支持附件）
- ✅ 查看邮箱中最近的邮件主题与编号
- ✅ 下载指定邮件中的所有附件
- ✅ 支持命令行参数和帮助信息

## 🔧 使用方法

```bash
# 运行命令并发送日志
python run_with_mail_notify.py run "command" result.log

# 手动发送一封邮件
python run_with_mail_notify.py send "主题" "正文内容" result.log

# 查看最近 5 封邮件
python run_with_mail_notify.py inbox 5

# 下载邮件编号为 1234 的所有附件
python run_with_mail_notify.py download 1234 ./attachments

# 查看帮助
python run_with_mail_notify.py -h
```

## 🔐 邮箱配置
### 你需要在代码中设置以下参数来完成邮箱功能的启用
```bash
# 发件人邮箱账户（企业邮箱或支持SMTP/IMAP的邮箱）
smtp_server = "smtp.exmail.qq.com"         # 邮件发送服务器地址（SMTP）
smtp_port = 465                            # SMTP端口（通常为465，SSL加密）
imap_server = "imap.exmail.qq.com"         # 邮件接收服务器地址（IMAP）
sender_email = "你的邮箱地址"                # 发件人邮箱
sender_password = os.getenv("EMAIL_PASS")  # 从环境变量中读取邮箱授权码/密码
receiver_email = "你的邮箱地址"              # 接收人邮箱地址
```

### 📌 建议使用环境变量 EMAIL_PASS 储存授权码，而不是将密码写入代码，提升安全性。
```bash
export EMAIL_PASS="邮箱授权码"
```
