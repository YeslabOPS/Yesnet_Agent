import { useState } from 'react';
import { useRouter } from 'next/router';
import styles from '../styles/Login.module.css';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleLogin = () => {
    // 简单的登录逻辑，实际应用中应使用更安全的认证方式
    if (username === 'admin' && password === 'password') {
      router.push('/manage');
    } else {
      alert('用户名或密码错误');
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.loginBox}>
        <h1>登录</h1>
        <input
          type="text"
          placeholder="用户名"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className={styles.input}
        />
        <input
          type="password"
          placeholder="密码"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={styles.input}
        />
        <button onClick={handleLogin} className={styles.button}>登录</button>
      </div>
    </div>
  );
} 