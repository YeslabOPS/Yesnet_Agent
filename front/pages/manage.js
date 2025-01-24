import { useEffect, useState } from 'react';
import axios from 'axios';
import MindMap from '../components/MindMap';

export default function Manage() {
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    // 获取Zabbix监控指标
    axios.get('http://127.0.0.1:8000/api/zabbix/metrics')
      .then(response => {
        setMetrics(response.data);
      })
      .catch(error => {
        console.error('获取监控指标失败:', error);
      });
  }, []);

  return (
    <div>
      <h1>管理页面</h1>
      <MindMap data={metrics} />
    </div>
  );
} 