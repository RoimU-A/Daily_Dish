#!/bin/bash

# Daily Dish ngrok本番稼働スクリプト

echo "Daily Dish ngrok本番稼働を開始します..."
echo "=========================================="

# 環境変数設定
export NGROK_MODE=true

# プロセス確認・停止
echo "既存のプロセスを確認中..."
pkill -f "python manage.py runserver" 2>/dev/null
pkill -f "ngrok http" 2>/dev/null
sleep 2

# Djangoサーバーをバックグラウンドで起動
echo "Djangoサーバーを起動中..."
python manage.py runserver 0.0.0.0:8000 > django_production.log 2>&1 &
DJANGO_PID=$!

# 少し待ってからDjangoサーバーの起動確認
sleep 3
if ps -p $DJANGO_PID > /dev/null; then
    echo "✅ Djangoサーバー起動成功 (PID: $DJANGO_PID)"
else
    echo "❌ Djangoサーバー起動失敗"
    exit 1
fi

# ngrok起動（フォアグラウンドで実行）
echo "ngrokを起動中..."
echo "生成されたURLをメモしてください："
echo "------------------------------------------"
./ngrok http 8000

# 終了処理（Ctrl+Cで停止した時）
echo ""
echo "ngrok停止中..."
kill $DJANGO_PID 2>/dev/null
echo "Daily Dish ngrok稼働を停止しました"