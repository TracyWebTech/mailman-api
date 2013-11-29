Received: by {{ip_from}} with HTTP;
        {{timestamp}}
% if defined('in_reply_to'):
In-Reply-To: {{!in_reply_to}}
% end
Content-Type: text/plain; charset=UTF-8
From: {{name_from}} <{{email_from}}>
To: {{email_to}}
Message-ID: <{{message_id}}>
Subject: {{subject}}

{{body}}
