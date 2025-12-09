class CurveDrawer {
      constructor(canvasId) {
        this.canvas = document.getElementById("canvas");
        this.ctx = this.canvas.getContext('2d');
        this.points = [];
        this.curveDrawn = false;
        this.pointRadius = 6;
        this.lineWidth = 2.5;

        this.setupCanvas();
        this.setupEventListeners();
        this.setupButtons();
        this.draw();
      }

      setupCanvas() {
        const rect = this.canvas.getBoundingClientRect();
        this.canvas.width = rect.width;
        this.canvas.height = rect.height;
      }

      setupEventListeners() {
        this.canvas.addEventListener('click', (e) => this.handleCanvasClick(e));
        window.addEventListener('resize', () => {
          this.setupCanvas();
          this.draw();
        });
      }

      setupButtons() {
        document.getElementById('drawBtn').addEventListener('click', () => this.drawCurve());
        document.getElementById('undoBtn').addEventListener('click', () => this.undoPoint());
        document.getElementById('clearBtn').addEventListener('click', () => this.clear());
      }

      handleCanvasClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        this.addPoint(x, y);
      }

      addPoint(x, y) {
        this.points.push({ x, y });
        this.curveDrawn = false;
        this.draw();
        this.updatePointCount();
      }

      undoPoint() {
        if (this.points.length > 0) {
          this.points.pop();
          this.curveDrawn = false;
          this.draw();
          this.updatePointCount();
        }
      }

      clear() {
        this.points = [];
        this.curveDrawn = false;
        this.draw();
        this.updatePointCount();
      }

      drawCurve() {
        if (this.points.length < 2) {
          alert('Please add at least 2 points');
          return;
        }
        this.curveDrawn = true;
        this.draw();
      }

      catmullRom(p0, p1, p2, p3, t) {
        const t2 = t * t;
        const t3 = t2 * t;

        return (
          0.5 *
          (2 * p1 +
            (-p0 + p2) * t +
            (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
            (-p0 + 3 * p1 - 3 * p2 + p3) * t3)
        );
      }

      getCurvePoints() {
        if (!this.curveDrawn || this.points.length < 2) {
          return this.points;
        }

        const curvePoints = [];
        const resolution = 50;

        for (let i = 0; i < this.points.length - 1; i++) {
          const p0 = this.points[Math.max(0, i - 1)];
          const p1 = this.points[i];
          const p2 = this.points[i + 1];
          const p3 = this.points[Math.min(this.points.length - 1, i + 2)];

          for (let t = 0; t < 1; t += 1 / resolution) {
            const x = this.catmullRom(p0.x, p1.x, p2.x, p3.x, t);
            const y = this.catmullRom(p0.y, p1.y, p2.y, p3.y, t);
            curvePoints.push({ x, y });
          }
        }

        return curvePoints;
      }

      draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        const curvePoints = this.getCurvePoints();

        if (this.curveDrawn && curvePoints.length > 1) {
          this.ctx.strokeStyle = '#3b82f6';
          this.ctx.lineWidth = 2;
          this.ctx.beginPath();
          this.ctx.moveTo(curvePoints[0].x, curvePoints[0].y);

          for (let i = 1; i < curvePoints.length; i++) {
            this.ctx.lineTo(curvePoints[i].x, curvePoints[i].y);
          }
          this.ctx.stroke();
        }

        this.ctx.fillStyle = '#ef4444';
        this.ctx.beginPath();
        for (const point of this.points) {
          this.ctx.moveTo(point.x + 5, point.y);
          this.ctx.arc(point.x, point.y, 5, 0, Math.PI * 2);
        }
        this.ctx.fill();
      }

      updatePointCount() {
        document.getElementById('pointCount').textContent = this.points.length;
      }
    }

    new CurveDrawer();

