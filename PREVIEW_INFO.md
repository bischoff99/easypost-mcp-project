# 🚀 Production Preview - Running!

**Started**: $(date '+%Y-%m-%d %H:%M:%S')

---

## 🌐 Access URLs

### Frontend (Production Build)
- **URL**: http://localhost:4173
- **Server**: Vite Preview (serving dist/)
- **Status**: ✅ Running

### Backend API
- **URL**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health**: http://localhost:8000/health
- **Metrics**: http://localhost:8000/metrics
- **Status**: ✅ Running

---

## 🧪 Test Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Create Shipment
```bash
curl -X POST http://localhost:8000/api/shipments \
  -H "Content-Type: application/json" \
  -d '{
    "to_address": {
      "name": "John Doe",
      "street1": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zip": "10001"
    },
    "from_address": {
      "name": "Jane Smith",
      "street1": "456 Market St",
      "city": "San Francisco",
      "state": "CA",
      "zip": "94102"
    },
    "parcel": {
      "length": 10,
      "width": 8,
      "height": 6,
      "weight": 16
    }
  }'
```

### Get Tracking
```bash
curl http://localhost:8000/api/tracking/EZ1234567890
```

### Get Rates
```bash
curl -X POST http://localhost:8000/api/rates \
  -H "Content-Type: application/json" \
  -d '{
    "to_address": {...},
    "from_address": {...},
    "parcel": {...}
  }'
```

---

## 📱 Frontend Pages

Visit these URLs in your browser:

- **Dashboard**: http://localhost:4173/
- **Shipments**: http://localhost:4173/shipments
- **Tracking**: http://localhost:4173/tracking
- **Analytics**: http://localhost:4173/analytics
- **Address Book**: http://localhost:4173/addresses
- **Settings**: http://localhost:4173/settings

---

## 🔍 Features to Test

### Dashboard
- ✅ Animated stats cards
- ✅ Quick action cards
- ✅ Recent activity feed
- ✅ Carrier performance charts

### Shipments
- ✅ Advanced data table
- ✅ Search and filters
- ✅ Row selection
- ✅ Bulk actions UI

### Tracking
- ✅ Tracking number lookup
- ✅ Timeline visualization
- ✅ Status updates
- ✅ Delivery estimates

### Analytics
- ✅ Recharts visualizations
- ✅ Volume trends
- ✅ Carrier distribution
- ✅ Cost breakdown (pie chart)
- ✅ Top destinations

### Address Book
- ✅ Address card grid
- ✅ Search functionality
- ✅ Default address badge
- ✅ CRUD UI (edit/delete)

### Settings
- ✅ Account information
- ✅ API configuration
- ✅ Notification preferences
- ✅ Theme selection

---

## 🛑 Stop Servers

When done testing:
```bash
# Find and kill background processes
ps aux | grep -E "(python src/server|vite preview)" | grep -v grep

# Or use:
pkill -f "python src/server"
pkill -f "vite preview"
```

---

## ✅ Production Build Verified

- ✅ Frontend build successful (1.64s)
- ✅ Backend imports successfully
- ✅ All routes registered
- ✅ Health checks active
- ✅ Zero vulnerabilities
- ✅ All tests passing

**Ready for production deployment!**
