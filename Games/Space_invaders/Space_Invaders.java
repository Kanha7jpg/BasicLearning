import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Random;

public class SpaceInvaders extends JPanel implements ActionListener, KeyListener {

    // ── constants ──────────────────────────────────────────────
    static final int W = 800, H = 650;
    static final int ALIEN_COLS = 11, ALIEN_ROWS = 5;
    static final int ALIEN_W = 40, ALIEN_H = 30;
    static final int ALIEN_H_GAP = 55, ALIEN_V_GAP = 45;
    static final int PLAYER_W = 52, PLAYER_H = 28;
    static final int BULLET_W = 4, BULLET_H = 14;
    static final int BOMB_W = 5, BOMB_H = 14;
    static final int SHIELD_BLOCK = 8;
    static final int PLAYER_SPEED = 5;
    static final int BULLET_SPEED = 11;
    static final int BOMB_SPEED = 4;
    static final int ALIEN_DROP = 18;
    static final int TICK = 16; // ~62fps

    // ── state ──────────────────────────────────────────────────
    int playerX;
    boolean left, right, shooting;
    long lastShot;

    ArrayList<int[]> aliens   = new ArrayList<>(); // [x,y,type,alive]
    ArrayList<int[]> bullets  = new ArrayList<>(); // [x,y]
    ArrayList<int[]> bombs    = new ArrayList<>(); // [x,y]
    ArrayList<int[]> shields  = new ArrayList<>(); // [x,y,hp]  hp 1‑3

    int alienDX = 1;
    long lastAlienMove;
    int alienMoveInterval = 700; // ms; speeds up as aliens die

    // UFO
    int ufox = -1;
    boolean ufoDirRight;
    long lastUfo;
    int ufoScore = 0;
    long ufoFlashUntil = 0;

    int score = 0, lives = 3, level = 1;
    boolean gameOver = false, won = false, paused = false;

    Timer timer;
    Random rng = new Random();

    // ── colors ─────────────────────────────────────────────────
    static final Color BG       = new Color(5, 5, 20);
    static final Color C_PLAYER = new Color(100, 220, 100);
    static final Color C_BULLET = new Color(255, 255, 120);
    static final Color C_BOMB   = new Color(255, 80,  80);
    static final Color C_UFO    = new Color(220, 50, 220);
    static final Color C_SHIELD = new Color(60, 200, 60);
    static final Color C_HUD    = new Color(180, 230, 180);
    static final Color[] ALIEN_COLORS = {
        new Color(255, 100, 100),
        new Color(255, 180, 60),
        new Color(100, 180, 255),
        new Color(200, 100, 255),
        new Color(80,  220, 200)
    };

    // ── constructor ────────────────────────────────────────────
    public SpaceInvaders() {
        setPreferredSize(new Dimension(W, H));
        setBackground(BG);
        setFocusable(true);
        addKeyListener(this);
        initGame();
        timer = new Timer(TICK, this);
        timer.start();
    }

    void initGame() {
        playerX = W / 2 - PLAYER_W / 2;
        bullets.clear(); bombs.clear();
        buildAliens();
        buildShields();
        lastAlienMove = System.currentTimeMillis();
        alienMoveInterval = Math.max(150, 700 - (level - 1) * 80);
        lastUfo = System.currentTimeMillis() + 5000;
        ufox = -1;
        gameOver = false; won = false;
        left = right = shooting = false;
        lastShot = 0;
    }

    void buildAliens() {
        aliens.clear();
        int startX = (W - ALIEN_COLS * ALIEN_H_GAP) / 2 + 10;
        int startY = 80;
        for (int r = 0; r < ALIEN_ROWS; r++)
            for (int c = 0; c < ALIEN_COLS; c++)
                aliens.add(new int[]{startX + c * ALIEN_H_GAP, startY + r * ALIEN_V_GAP, r, 1});
    }

    void buildShields() {
        shields.clear();
        int[] shieldX = {110, 270, 430, 590};
        int sy = H - 140;
        int bw = 8, bh = 5; // blocks wide/tall per shield
        for (int sx : shieldX)
            for (int bx = 0; bx < bw; bx++)
                for (int by = 0; by < bh; by++) {
                    // notch in middle-bottom
                    if (by >= 3 && bx >= 3 && bx <= 4) continue;
                    shields.add(new int[]{sx + bx * SHIELD_BLOCK, sy + by * SHIELD_BLOCK, 3});
                }
    }

    // ── main loop ──────────────────────────────────────────────
    @Override
    public void actionPerformed(ActionEvent e) {
        if (gameOver || won || paused) { repaint(); return; }

        movePlayer();
        moveBullets();
        moveBombs();
        moveAliens();
        moveUfo();
        checkCollisions();
        alienShoot();
        checkWinLose();
        repaint();
    }

    void movePlayer() {
        if (left  && playerX > 0)          playerX -= PLAYER_SPEED;
        if (right && playerX < W - PLAYER_W) playerX += PLAYER_SPEED;
        long now = System.currentTimeMillis();
        if (shooting && now - lastShot > 400 && bullets.size() < 3) {
            bullets.add(new int[]{playerX + PLAYER_W / 2 - BULLET_W / 2, H - 90});
            lastShot = now;
        }
    }

    void moveBullets() {
        Iterator<int[]> it = bullets.iterator();
        while (it.hasNext()) { int[] b = it.next(); b[1] -= BULLET_SPEED; if (b[1] < 0) it.remove(); }
    }

    void moveBombs() {
        Iterator<int[]> it = bombs.iterator();
        while (it.hasNext()) {
            int[] b = it.next(); b[1] += BOMB_SPEED;
            if (b[1] > H) it.remove();
        }
    }

    void moveAliens() {
        long now = System.currentTimeMillis();
        if (now - lastAlienMove < alienMoveInterval) return;
        lastAlienMove = now;

        // check edges
        boolean hitEdge = false;
        for (int[] a : aliens) {
            if (a[3] == 0) continue;
            if (alienDX > 0 && a[0] + ALIEN_W + alienDX > W - 10) { hitEdge = true; break; }
            if (alienDX < 0 && a[0] + alienDX < 10)                 { hitEdge = true; break; }
        }
        if (hitEdge) {
            for (int[] a : aliens) a[1] += ALIEN_DROP;
            alienDX = -alienDX;
        } else {
            for (int[] a : aliens) a[0] += alienDX * 6;
        }

        // speed up proportional to kills
        long alive = aliens.stream().filter(a -> a[3] == 1).count();
        int total  = ALIEN_COLS * ALIEN_ROWS;
        double frac = 1.0 - (double) alive / total;
        alienMoveInterval = (int) Math.max(80, (700 - (level - 1) * 80) * (1.0 - frac * 0.85));
    }

    void moveUfo() {
        long now = System.currentTimeMillis();
        if (ufox < 0) {
            if (now > lastUfo + 15000 + rng.nextInt(10000)) {
                ufox = ufoDirRight ? 0 : W;
                ufoDirRight = rng.nextBoolean();
                ufox = ufoDirRight ? -60 : W + 10;
            }
            return;
        }
        ufox += ufoDirRight ? 2 : -2;
        if (ufox > W + 80 || ufox < -80) {
            ufox = -1;
            lastUfo = now;
        }
    }

    void alienShoot() {
        // random alien in bottom row of each column shoots
        if (rng.nextInt(100) < 2 + level) {
            ArrayList<int[]> candidates = new ArrayList<>();
            for (int c = 0; c < ALIEN_COLS; c++) {
                int[] lowest = null;
                for (int[] a : aliens)
                    if (a[3] == 1 && a[0] / ALIEN_H_GAP == c || sameCol(a, c))
                        if (lowest == null || a[1] > lowest[1]) lowest = a;
                if (lowest != null) candidates.add(lowest);
            }
            if (!candidates.isEmpty()) {
                int[] shooter = candidates.get(rng.nextInt(candidates.size()));
                bombs.add(new int[]{shooter[0] + ALIEN_W / 2 - BOMB_W / 2, shooter[1] + ALIEN_H});
            }
        }
    }

    boolean sameCol(int[] a, int col) {
        int startX = (W - ALIEN_COLS * ALIEN_H_GAP) / 2 + 10;
        return Math.abs(a[0] - (startX + col * ALIEN_H_GAP)) < ALIEN_H_GAP;
    }

    void checkCollisions() {
        // bullet vs alien
        Iterator<int[]> bit = bullets.iterator();
        while (bit.hasNext()) {
            int[] b = bit.next();
            boolean hit = false;
            for (int[] a : aliens) {
                if (a[3] == 0) continue;
                if (overlaps(b[0], b[1], BULLET_W, BULLET_H, a[0], a[1], ALIEN_W, ALIEN_H)) {
                    a[3] = 0; hit = true;
                    score += (ALIEN_ROWS - a[2]) * 10 * level;
                    break;
                }
            }
            // bullet vs shield
            if (!hit) {
                Iterator<int[]> sit = shields.iterator();
                while (sit.hasNext()) {
                    int[] s = sit.next();
                    if (overlaps(b[0], b[1], BULLET_W, BULLET_H, s[0], s[1], SHIELD_BLOCK, SHIELD_BLOCK)) {
                        s[2]--; if (s[2] <= 0) sit.remove();
                        hit = true; break;
                    }
                }
            }
            // bullet vs ufo
            if (!hit && ufox >= 0) {
                if (overlaps(b[0], b[1], BULLET_W, BULLET_H, ufox, 30, 60, 22)) {
                    ufoScore = (rng.nextInt(6) + 1) * 50;
                    score += ufoScore;
                    ufoFlashUntil = System.currentTimeMillis() + 900;
                    ufox = -1; lastUfo = System.currentTimeMillis();
                    hit = true;
                }
            }
            if (hit) bit.remove();
        }

        // bomb vs player
        int px = playerX, py = H - 80;
        Iterator<int[]> boit = bombs.iterator();
        while (boit.hasNext()) {
            int[] b = boit.next();
            // bomb vs shield
            boolean hit = false;
            Iterator<int[]> sit = shields.iterator();
            while (sit.hasNext()) {
                int[] s = sit.next();
                if (overlaps(b[0], b[1], BOMB_W, BOMB_H, s[0], s[1], SHIELD_BLOCK, SHIELD_BLOCK)) {
                    s[2]--; if (s[2] <= 0) sit.remove();
                    hit = true; break;
                }
            }
            if (!hit && overlaps(b[0], b[1], BOMB_W, BOMB_H, px, py, PLAYER_W, PLAYER_H)) {
                lives--;
                if (lives <= 0) { gameOver = true; timer.stop(); }
                else { playerX = W / 2 - PLAYER_W / 2; bullets.clear(); bombs.clear(); }
                hit = true;
            }
            if (hit) boit.remove();
        }
    }

    void checkWinLose() {
        long alive = aliens.stream().filter(a -> a[3] == 1).count();
        if (alive == 0) { won = true; return; }
        // alien reaches bottom
        for (int[] a : aliens)
            if (a[3] == 1 && a[1] + ALIEN_H >= H - 90) { gameOver = true; timer.stop(); return; }
    }

    boolean overlaps(int x1,int y1,int w1,int h1, int x2,int y2,int w2,int h2) {
        return x1 < x2+w2 && x1+w1 > x2 && y1 < y2+h2 && y1+h1 > y2;
    }

    // ── rendering ─────────────────────────────────────────────
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        drawStars(g2);

        if (gameOver) { drawOverlay(g2, "GAME OVER", "Score: " + score, "Press R to restart"); return; }
        if (won)      { drawOverlay(g2, "YOU WIN!",  "Score: " + score, "Press N for next level  |  R to restart"); return; }
        if (paused)   { drawOverlay(g2, "PAUSED",    "",                "Press P to resume"); return; }

        drawShields(g2);
        drawAliens(g2);
        drawUfo(g2);
        drawBullets(g2);
        drawBombs(g2);
        drawPlayer(g2);
        drawHUD(g2);
    }

    void drawStars(Graphics2D g) {
        g.setColor(new Color(255, 255, 255, 60));
        rng.setSeed(42);
        for (int i = 0; i < 120; i++)
            g.fillOval(rng.nextInt(W), rng.nextInt(H), 1 + rng.nextInt(2), 1 + rng.nextInt(2));
        rng.setSeed(System.currentTimeMillis() / 1000); // restore
    }

    void drawAliens(Graphics2D g) {
        long frame = System.currentTimeMillis() / 400;
        for (int[] a : aliens) {
            if (a[3] == 0) continue;
            g.setColor(ALIEN_COLORS[a[2]]);
            drawAlienShape(g, a[0], a[1], a[2], (int)(frame % 2));
        }
    }

    void drawAlienShape(Graphics2D g, int x, int y, int type, int frame) {
        // draw different pixelart-ish shapes per row type
        switch (type) {
            case 0: // top row – small squid
                g.fillRect(x+14, y+2, 12, 8);
                g.fillRect(x+8,  y+8, 24, 8);
                g.fillRect(x+4,  y+14, 8, 6); g.fillRect(x+28, y+14, 8, 6);
                if (frame==0) { g.fillRect(x+2, y+20, 6, 4); g.fillRect(x+32, y+20, 6, 4); }
                else          { g.fillRect(x+6, y+22, 6, 4); g.fillRect(x+28, y+22, 6, 4); }
                break;
            case 1: case 2: // middle rows – crab
                g.fillRect(x+6,  y+2,  28, 8);
                g.fillRect(x+2,  y+8,  36, 10);
                g.fillRect(x+6,  y+18, 8,  6); g.fillRect(x+26, y+18, 8, 6);
                if (frame==0) { g.fillRect(x+2, y+22, 6, 6); g.fillRect(x+32, y+22, 6, 6); }
                else          { g.fillRect(x+0, y+20, 6, 6); g.fillRect(x+34, y+20, 6, 6); }
                break;
            default: // bottom rows – octopus
                g.fillRect(x+10, y+2,  20, 6);
                g.fillRect(x+4,  y+6,  32, 10);
                g.fillRect(x+2,  y+14, 36, 8);
                g.fillRect(x+4,  y+22, 8,  6); g.fillRect(x+28, y+22, 8, 6);
                if (frame==0) { g.fillRect(x+2, y+26, 5, 4); g.fillRect(x+33, y+26, 5, 4); }
                else          { g.fillRect(x+4, y+28, 5, 4); g.fillRect(x+31, y+28, 5, 4); }
        }
    }

    void drawUfo(Graphics2D g) {
        long now = System.currentTimeMillis();
        if (now < ufoFlashUntil) {
            // show score flash
            g.setFont(new Font("Courier New", Font.BOLD, 18));
            g.setColor(C_UFO);
            g.drawString("+" + ufoScore, W / 2 - 20, 48);
        }
        if (ufox < 0) return;
        g.setColor(C_UFO);
        g.fillOval(ufox + 10, 34, 40, 16);
        g.fillOval(ufox + 20, 26, 22, 16);
        g.setColor(C_UFO.brighter());
        g.fillOval(ufox + 14, 38, 8, 6);
        g.fillOval(ufox + 26, 38, 8, 6);
        g.fillOval(ufox + 38, 38, 8, 6);
    }

    void drawPlayer(Graphics2D g) {
        int x = playerX, y = H - 80;
        g.setColor(C_PLAYER);
        // body
        g.fillRect(x + 4,  y + 10, PLAYER_W - 8, PLAYER_H - 10);
        // cannon
        g.fillRect(x + 22, y,      8,             14);
        // nozzle
        g.setColor(C_PLAYER.brighter());
        g.fillRect(x + 23, y - 4,  6,             6);
        // engine glow
        g.setColor(new Color(80, 255, 80, 100));
        g.fillRect(x + 10, y + PLAYER_H, PLAYER_W - 20, 6);
    }

    void drawBullets(Graphics2D g) {
        g.setColor(C_BULLET);
        for (int[] b : bullets) {
            g.fillRect(b[0], b[1], BULLET_W, BULLET_H);
            g.setColor(new Color(255, 255, 180, 80));
            g.fillRect(b[0] - 2, b[1] + BULLET_H, BULLET_W + 4, 6);
            g.setColor(C_BULLET);
        }
    }

    void drawBombs(Graphics2D g) {
        g.setColor(C_BOMB);
        for (int[] b : bombs) {
            g.fillRect(b[0], b[1], BOMB_W, BOMB_H);
            // zigzag effect
            g.setColor(new Color(255, 160, 40));
            g.drawLine(b[0], b[1], b[0] + BOMB_W, b[1] + BOMB_H / 2);
            g.drawLine(b[0] + BOMB_W, b[1] + BOMB_H / 2, b[0], b[1] + BOMB_H);
            g.setColor(C_BOMB);
        }
    }

    void drawShields(Graphics2D g) {
        for (int[] s : shields) {
            int alpha = 80 + s[2] * 55; // fade as damaged
            g.setColor(new Color(60, 200, 60, Math.min(255, alpha)));
            g.fillRect(s[0], s[1], SHIELD_BLOCK, SHIELD_BLOCK);
        }
    }

    void drawHUD(Graphics2D g) {
        g.setFont(new Font("Courier New", Font.BOLD, 18));
        g.setColor(C_HUD);
        g.drawString("SCORE " + score, 20, 26);
        g.drawString("LEVEL " + level, W / 2 - 40, 26);
        // lives as little ships
        g.drawString("LIVES", W - 160, 26);
        for (int i = 0; i < lives; i++) {
            int lx = W - 80 + i * 24, ly = 10;
            g.setColor(C_PLAYER);
            g.fillRect(lx + 4, ly + 8, 14, 10);
            g.fillRect(lx + 8, ly + 2, 6, 8);
        }
        // divider
        g.setColor(new Color(60, 180, 60, 120));
        g.fillRect(0, 34, W, 2);
        // floor line
        g.fillRect(0, H - 54, W, 2);
    }

    void drawOverlay(Graphics2D g, String title, String sub, String hint) {
        g.setColor(new Color(0, 0, 0, 180));
        g.fillRect(0, 0, W, H);
        g.setFont(new Font("Courier New", Font.BOLD, 52));
        g.setColor(Color.WHITE);
        FontMetrics fm = g.getFontMetrics();
        g.drawString(title, (W - fm.stringWidth(title)) / 2, H / 2 - 60);
        if (!sub.isEmpty()) {
            g.setFont(new Font("Courier New", Font.PLAIN, 26));
            fm = g.getFontMetrics();
            g.setColor(C_HUD);
            g.drawString(sub, (W - fm.stringWidth(sub)) / 2, H / 2);
        }
        g.setFont(new Font("Courier New", Font.PLAIN, 18));
        fm = g.getFontMetrics();
        g.setColor(new Color(180, 180, 180));
        g.drawString(hint, (W - fm.stringWidth(hint)) / 2, H / 2 + 50);
    }

    // ── input ─────────────────────────────────────────────────
    @Override public void keyPressed(KeyEvent e) {
        int k = e.getKeyCode();
        if (k == KeyEvent.VK_LEFT  || k == KeyEvent.VK_A) left     = true;
        if (k == KeyEvent.VK_RIGHT || k == KeyEvent.VK_D) right    = true;
        if (k == KeyEvent.VK_SPACE || k == KeyEvent.VK_UP) shooting = true;
        if (k == KeyEvent.VK_P) paused = !paused;
        if (k == KeyEvent.VK_R) { lives = 3; score = 0; level = 1; initGame(); timer.start(); }
        if (k == KeyEvent.VK_N && won) { level++; initGame(); timer.start(); }
    }
    @Override public void keyReleased(KeyEvent e) {
        int k = e.getKeyCode();
        if (k == KeyEvent.VK_LEFT  || k == KeyEvent.VK_A) left     = false;
        if (k == KeyEvent.VK_RIGHT || k == KeyEvent.VK_D) right    = false;
        if (k == KeyEvent.VK_SPACE || k == KeyEvent.VK_UP) shooting = false;
    }
    @Override public void keyTyped(KeyEvent e) {}

    // ── entry point ───────────────────────────────────────────
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Space Invaders");
            SpaceInvaders game = new SpaceInvaders();
            frame.add(game);
            frame.pack();
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setResizable(false);
            frame.setLocationRelativeTo(null);

            // controls hint in title bar
            frame.setTitle("Space Invaders  |  ← → / A D to move  |  SPACE to shoot  |  P pause  |  R restart");
            frame.setVisible(true);
            game.requestFocusInWindow();
        });
    }
}