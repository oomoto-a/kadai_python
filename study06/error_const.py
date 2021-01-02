# -*- coding: utf-8 -*-


        error_message = {}
        error_message[400] = {"contents":"パラメーターエラー (必須パラメータ不足)", "Coping":"必須パラメータを設定してください。"}
        error_message[404] = {"contents":"対象のデータが存在しなかった場合", "Coping":"検索条件を変えてください"}
        error_message[429] = {"contents":"リクエスト過多 (各ユーザ制限値超過)", "Coping":"APIリクエスト数が上限に達した場合のエラーです。しばらく時間を空けてから、ご利用ください。"}
        error_message[500] = {"contents":"楽天ウェブサービス内のエラー", "Coping":"システムエラー。長時間続くようであれば、お問い合わせください。"}
        error_message[503] = {"contents":"メンテナンス・リクエスト過多(全ユーザ制限値超過)", "Coping":"このAPIはメンテナンス中です。"}
        
