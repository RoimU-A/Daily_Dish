const TestPage = () => {
  return (
    <div className="min-h-screen bg-sage-500 p-8">
      <h1 className="text-4xl text-white font-bold">TailwindCSS テスト</h1>
      <div className="bg-warm-200 p-4 mt-4 rounded">
        <p className="text-stone-800">カスタムカラーが表示されているかテスト</p>
      </div>
      <div className="bg-blue-500 p-4 mt-4 rounded">
        <p className="text-white">標準カラーが表示されているかテスト</p>
      </div>
    </div>
  );
};

export default TestPage;