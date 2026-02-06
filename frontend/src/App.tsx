import { useEffect, useState } from 'react'

type Offer = {
  id: number
  title: string
  reward_pro: number
  link: string
}

type User = {
  id: number
  balance_pro: number
  is_deposit: boolean
}

const tabs = ['Головна', 'Заробити', 'Гаманець'] as const

declare global {
  interface Window {
    Telegram?: {
      WebApp?: {
        initData: string
        ready: () => void
      }
    }
  }
}

export default function App() {
  const [activeTab, setActiveTab] = useState<typeof tabs[number]>('Головна')
  const [offers, setOffers] = useState<Offer[]>([])
  const [user, setUser] = useState<User | null>(null)
  const [userId, setUserId] = useState<number | null>(null)

  useEffect(() => {
    const initData = window.Telegram?.WebApp?.initData || ''
    window.Telegram?.WebApp?.ready()

    fetch('/api/auth', { headers: { initData } })
      .then((res) => res.json())
      .then((data) => {
        setUserId(data.id)
        setUser(data)
      })
      .catch(() => setUser(null))
  }, [])

  useEffect(() => {
    fetch('/api/offers')
      .then((res) => res.json())
      .then(setOffers)
      .catch(() => setOffers([]))
  }, [])

  useEffect(() => {
    if (!userId) return
    fetch('/api/me', { headers: { 'X-User-Id': String(userId) } })
      .then((res) => res.json())
      .then(setUser)
      .catch(() => setUser(null))
  }, [userId])

  const balanceUsd = user ? (user.balance_pro / 10000).toFixed(2) : '0.00'

  return (
    <div className="min-h-screen px-4 py-6">
      <header className="mb-6">
        <h1 className="text-2xl font-semibold">Casino WebApp</h1>
        <p className="text-sm text-slate-400">Ласкаво просимо до екосистеми бонусів.</p>
      </header>

      <nav className="flex gap-2 mb-6">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-full text-sm ${
              activeTab === tab ? 'bg-emerald-500 text-white' : 'bg-slate-800 text-slate-200'
            }`}
          >
            {tab}
          </button>
        ))}
      </nav>

      {activeTab === 'Головна' && (
        <section className="space-y-6">
          <div className="rounded-2xl bg-slate-900 p-4">
            <h2 className="text-lg font-semibold">Бонусна гра</h2>
            {user?.is_deposit ? (
              <p className="text-sm text-slate-300 mt-2">Ви активували бонус. Грайте та отримуйте нагороди.</p>
            ) : (
              <p className="text-sm text-slate-400 mt-2">Бонусна гра доступна після депозиту.</p>
            )}
          </div>
          <div className="rounded-2xl bg-slate-900 p-4">
            <h2 className="text-lg font-semibold">Пропозиції</h2>
            <ul className="mt-4 space-y-3">
              {offers.map((offer) => (
                <li key={offer.id} className="flex items-center justify-between bg-slate-800/60 p-3 rounded-xl">
                  <div>
                    <p className="font-medium">{offer.title}</p>
                    <p className="text-xs text-slate-400">Нагорода: {offer.reward_pro} PRO</p>
                  </div>
                  <a
                    href={offer.link}
                    className="text-sm text-emerald-400"
                    target="_blank"
                    rel="noreferrer"
                  >
                    Відкрити
                  </a>
                </li>
              ))}
              {offers.length === 0 && <li className="text-sm text-slate-400">Поки немає пропозицій.</li>}
            </ul>
          </div>
        </section>
      )}

      {activeTab === 'Заробити' && (
        <section className="space-y-6">
          <div className="rounded-2xl bg-slate-900 p-4">
            <h2 className="text-lg font-semibold">Реферальне посилання</h2>
            <p className="text-sm text-slate-300 mt-2">Запросіть друзів та отримайте 1000 PRO.</p>
            <div className="mt-3 bg-slate-800 p-3 rounded-xl text-sm">
              https://t.me/your_bot?start=ref_12345
            </div>
          </div>
          <div className="rounded-2xl bg-slate-900 p-4">
            <h2 className="text-lg font-semibold">Статистика</h2>
            <p className="text-sm text-slate-400 mt-2">Запрошено друзів: 0</p>
          </div>
        </section>
      )}

      {activeTab === 'Гаманець' && (
        <section className="space-y-6">
          <div className="rounded-2xl bg-slate-900 p-4">
            <h2 className="text-lg font-semibold">Баланс</h2>
            <p className="text-2xl font-bold mt-2">{user?.balance_pro ?? 0} PRO</p>
            <p className="text-sm text-slate-400">≈ ${balanceUsd} USD</p>
          </div>
          <div className="rounded-2xl bg-slate-900 p-4">
            <h2 className="text-lg font-semibold">Вивід коштів</h2>
            <form className="mt-4 space-y-3">
              <input
                type="text"
                placeholder="Номер гаманця"
                className="w-full rounded-xl bg-slate-800 p-3 text-sm"
              />
              <input
                type="number"
                placeholder="Сума PRO"
                className="w-full rounded-xl bg-slate-800 p-3 text-sm"
              />
              <button type="button" className="w-full rounded-xl bg-emerald-500 py-2 text-sm font-semibold">
                Надіслати заявку
              </button>
            </form>
          </div>
        </section>
      )}
    </div>
  )
}
